"""Servidor MCP do plugin google-ads: lê a conta com GAQL e cria campanhas de Pesquisa pausadas.

Fluxo de escrita (obrigatório):
  1. simular_campanha_pesquisa(plano)  → valida localmente + validate_only na API, devolve um código
  2. o usuário revisa e dá ok
  3. criar_campanha_pesquisa(plano, codigo_confirmacao) → só aceita o MESMO plano já simulado
Configuração: ~/.config/google-ads-claude/config.json (ou GOOGLE_ADS_CLAUDE_CONFIG).
"""
import datetime as dt
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from google.ads.googleads.client import GoogleAdsClient  # noqa: E402
from google.ads.googleads.errors import GoogleAdsException  # noqa: E402
from google.protobuf import json_format  # noqa: E402
from mcp.server.mcpserver import MCPServer  # noqa: E402
from mcp.types import ToolAnnotations  # noqa: E402

import operacoes  # noqa: E402
from plano import PlanoCampanha, codigo, limpar_conta, normalizar, resumo, validar  # noqa: E402

CONFIG_PADRAO = "~/.config/google-ads-claude/config.json"
EXEMPLO_CONFIG = """{
  "json_key_file_path": "~/.config/google-ads-claude/credentials.json",
  "conta_padrao": "123-456-7890",
  "orcamento_diario_maximo": 100,
  "changelog": "~/google-ads-changelog.md"
}"""

mcp = MCPServer(
    "google-ads",
    instructions=(
        "Acesso à conta Google Ads do usuário. Leitura: consulta_gaql (valores *_micros ÷ 1.000.000). "
        "Escrita: sempre simular_campanha_pesquisa primeiro, mostrar o resumo ao usuário, e só chamar "
        "criar_campanha_pesquisa depois de um ok explícito dele, com o código devolvido pela simulação."
    ),
)
_simulados: dict[str, dict] = {}
_cache: dict = {}


class ErroConfig(Exception):
    pass


def _config() -> dict:
    caminho = os.path.expanduser(os.environ.get("GOOGLE_ADS_CLAUDE_CONFIG", CONFIG_PADRAO))
    if not os.path.exists(caminho):
        raise ErroConfig(f"Configuração não encontrada em {caminho}. Crie o arquivo assim:\n{EXEMPLO_CONFIG}\n"
                         "A chave JSON é a da conta de serviço do Google Cloud com acesso à conta do Google Ads.")
    with open(caminho, encoding="utf-8") as f:
        cfg = json.load(f)
    chave = os.path.expanduser(cfg.get("json_key_file_path", ""))
    if not os.path.exists(chave):
        raise ErroConfig(f"Chave da conta de serviço não encontrada: {chave or '(json_key_file_path vazio)'}")
    cfg["json_key_file_path"] = chave
    return cfg


def _cliente(cfg: dict) -> GoogleAdsClient:
    chave = (cfg["json_key_file_path"], cfg.get("login_customer_id"), cfg.get("developer_token"))
    if _cache.get("chave") != chave:
        d = {"json_key_file_path": cfg["json_key_file_path"], "use_proto_plus": True}
        if cfg.get("developer_token"):
            d["developer_token"] = cfg["developer_token"]
        if cfg.get("login_customer_id"):
            d["login_customer_id"] = limpar_conta(cfg["login_customer_id"])
        _cache.update(chave=chave, cliente=GoogleAdsClient.load_from_dict(d))
    return _cache["cliente"]


def _erro_api(ex: GoogleAdsException, rotulos: list[str] | None = None) -> str:
    linhas = []
    for e in ex.failure.errors:
        caminho, item = [], None
        for el in e.location.field_path_elements:
            tem_indice = type(el).pb(el).HasField("index")
            caminho.append(el.field_name + (f"[{el.index}]" if tem_indice else ""))
            if rotulos and el.field_name == "mutate_operations" and tem_indice and el.index < len(rotulos):
                item = rotulos[el.index]
        onde = f" em {item}" if item else ""
        campo = f" (campo {'.'.join(caminho)})" if caminho else ""
        linhas.append(f"- {e.message}{onde}{campo}")
    return f"A API do Google Ads recusou (request_id {ex.request_id}):\n" + "\n".join(linhas)


def _changelog(cfg: dict, texto: str) -> str:
    caminho = os.path.expanduser(cfg.get("changelog") or os.path.join(os.getcwd(), "google-ads-changelog.md"))
    novo = not os.path.exists(caminho)
    with open(caminho, "a", encoding="utf-8") as f:
        if novo:
            f.write("# Mudanças na conta Google Ads\n\n")
        f.write(texto + "\n")
    return caminho


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
def contas_acessiveis() -> str:
    """Lista as contas do Google Ads que a conta de serviço consegue acessar e a conta padrão configurada."""
    try:
        cfg = _config()
        cli = _cliente(cfg)
        nomes = [r.split("/")[-1] for r in cli.get_service("CustomerService").list_accessible_customers().resource_names]
        padrao = limpar_conta(cfg.get("conta_padrao"))
        if padrao and padrao not in nomes:
            nomes.append(padrao)
        svc = cli.get_service("GoogleAdsService")
        linhas = []
        for cid in nomes:
            try:
                q = "SELECT customer.id, customer.descriptive_name, customer.manager, customer.currency_code, " \
                    "customer.time_zone, customer.status FROM customer"
                r = next(iter(svc.search(customer_id=cid, query=q)))
                c = r.customer
                linhas.append(f"- {cid} {c.descriptive_name!r} · {c.status.name} · {c.currency_code} · {c.time_zone}"
                              f"{' · administradora' if c.manager else ''}{' · PADRÃO' if cid == padrao else ''}")
            except GoogleAdsException as ex:
                linhas.append(f"- {cid}: sem acesso ({ex.failure.errors[0].message})")
        return "\n".join(linhas) or "Nenhuma conta acessível."
    except ErroConfig as e:
        return str(e)
    except GoogleAdsException as ex:
        return _erro_api(ex)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
def consulta_gaql(consulta: str, conta: str | None = None, limite: int = 200) -> str:
    """Roda uma consulta GAQL (somente SELECT) e devolve as linhas em JSON.

    conta: ID da conta (com ou sem hífens); vazio = conta padrão. limite: máximo de linhas (até 10.000).
    Valores *_micros vêm em micros: divida por 1.000.000 para ter reais.
    """
    if not consulta.strip().lower().startswith("select"):
        return "Só consultas SELECT são aceitas."
    try:
        cfg = _config()
        cid = limpar_conta(conta or cfg.get("conta_padrao"))
        if len(cid) != 10:
            return "Informe a conta (10 dígitos) ou configure conta_padrao."
        limite = max(1, min(int(limite), 10_000))
        linhas, truncado = [], False
        for lote in _cliente(cfg).get_service("GoogleAdsService").search_stream(customer_id=cid, query=consulta):
            for row in lote.results:
                if len(linhas) >= limite:
                    truncado = True
                    break
                linhas.append(json_format.MessageToDict(type(row).pb(row), preserving_proto_field_name=True))
            if truncado:
                break
        return json.dumps({"conta": cid, "linhas": len(linhas), "truncado": truncado, "resultados": linhas},
                          ensure_ascii=False)
    except ErroConfig as e:
        return str(e)
    except GoogleAdsException as ex:
        return _erro_api(ex)


def _mutate(cli: GoogleAdsClient, conta: str, ops: list, validar_apenas: bool):
    req = cli.get_type("MutateGoogleAdsRequest")
    req.customer_id = conta
    req.mutate_operations.extend(ops)
    req.validate_only = validar_apenas
    return cli.get_service("GoogleAdsService").mutate(request=req)


def _preparar(plano: PlanoCampanha):
    cfg = _config()
    d = normalizar(plano, cfg.get("conta_padrao"))
    erros, avisos = validar(d, cfg.get("orcamento_diario_maximo"))
    return cfg, d, erros, avisos


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=True))
def simular_campanha_pesquisa(plano: PlanoCampanha) -> str:
    """Valida uma campanha de Pesquisa sem criar nada (checagem local + validate_only na API).

    Devolve o resumo para mostrar ao usuário e um código de confirmação. A campanha sempre nasce pausada.
    Mostre o resumo ao usuário e só chame criar_campanha_pesquisa depois do ok explícito dele.
    """
    try:
        cfg, d, erros, avisos = _preparar(plano)
    except ErroConfig as e:
        return str(e)
    txt_avisos = ("\n\nAvisos:\n" + "\n".join(f"- {a}" for a in avisos)) if avisos else ""
    if erros:
        return "Plano com erros (nada foi enviado à API):\n" + "\n".join(f"- {e}" for e in erros) + txt_avisos
    cli = _cliente(cfg)
    ops, rotulos = operacoes.montar(cli, d)
    try:
        _mutate(cli, d["conta"], ops, validar_apenas=True)
    except GoogleAdsException as ex:
        return _erro_api(ex, rotulos) + txt_avisos
    cod = codigo(d)
    _simulados[cod] = d
    return (f"Simulação aprovada pela API ({len(ops)} operações, nada foi criado).\n\n{resumo(d)}{txt_avisos}\n\n"
            f"Código de confirmação: {cod}\n"
            "Para criar, chame criar_campanha_pesquisa com o MESMO plano e este código, só depois do ok do usuário.")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=False,
                                      openWorldHint=True))
def criar_campanha_pesquisa(plano: PlanoCampanha, codigo_confirmacao: str) -> str:
    """Cria na conta a campanha de Pesquisa já simulada, PAUSADA. Só use após o ok explícito do usuário.

    Exige o código devolvido por simular_campanha_pesquisa para exatamente este plano; qualquer mudança
    no plano pede nova simulação. Registra a mudança no changelog.
    """
    try:
        cfg, d, erros, _ = _preparar(plano)
    except ErroConfig as e:
        return str(e)
    cod = codigo(d)
    if cod != codigo_confirmacao.strip():
        return "O plano mudou desde a simulação (o código não confere). Simule de novo e peça o ok ao usuário."
    if cod not in _simulados:
        return "Este plano não foi simulado nesta sessão do servidor. Rode simular_campanha_pesquisa antes."
    if erros:
        return "Plano com erros:\n" + "\n".join(f"- {e}" for e in erros)
    cli = _cliente(cfg)
    ops, rotulos = operacoes.montar(cli, d)
    try:
        resp = _mutate(cli, d["conta"], ops, validar_apenas=False)
    except GoogleAdsException as ex:
        return _erro_api(ex, rotulos)
    del _simulados[cod]

    criados = {}
    for r in resp.mutate_operation_responses:
        tipo = type(r).pb(r).WhichOneof("response")
        criados.setdefault(tipo, []).append(getattr(r, tipo).resource_name)
    campanha = criados.get("campaign_result", ["?"])[0]
    agora = dt.datetime.now().strftime("%Y-%m-%d %H:%M")
    n_kw = sum(len(g["palavras_chave"]) for g in d["grupos"])
    n_ad = sum(len(g["anuncios"]) for g in d["grupos"])
    registro = (f"## {agora} — campanha criada (pausada)\n"
                f"- Conta: {d['conta']}\n- Campanha: {d['nome']} ({campanha})\n"
                f"- Antes: não existia · Depois: PAUSADA, R$ {d['orcamento_diario']:.2f}/dia\n"
                f"- {len(d['grupos'])} grupos, {n_kw} palavras-chave, {n_ad} anúncios, {len(d['negativas'])} negativas\n"
                f"- Código da simulação: {cod}\n")
    try:
        onde = _changelog(cfg, registro)
    except OSError as e:
        onde = f"(não consegui gravar o changelog: {e})"
    return (f"Campanha criada PAUSADA: {campanha}\n{len(ops)} operações aplicadas. Registro em {onde}.\n"
            "Para ativar, revise na interface do Google Ads (extensões, conversões) e ative por lá.")


if __name__ == "__main__":
    mcp.run()
