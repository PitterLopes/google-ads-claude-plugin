"""Plano de campanha de Pesquisa: formato, validação local, código de confirmação e resumo.

Não fala com a API: tudo aqui é puro e testável sem credenciais.
As regras de texto vêm do validador do Editor (skills/create-campaign/scripts), para que
o CSV e a publicação direta sigam exatamente os mesmos limites.
"""
import hashlib
import json
import os
import re
import sys
from typing import Literal, Optional

from pydantic import BaseModel, Field

_SCRIPTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skills", "create-campaign", "scripts")
sys.path.insert(0, os.path.normpath(_SCRIPTS))
import validate_editor_csv as editor  # noqa: E402

BRASIL, PORTUGUES = 2076, 1014
MATCH = {"FRASE": "PHRASE", "EXATA": "EXACT", "AMPLA": "BROAD"}


class PalavraChave(BaseModel):
    texto: str
    correspondencia: Literal["FRASE", "EXATA", "AMPLA"] = "FRASE"


class Anuncio(BaseModel):
    """Anúncio responsivo de pesquisa (RSA)."""
    titulos: list[str] = Field(description="3 a 15 títulos, até 30 caracteres cada")
    descricoes: list[str] = Field(description="2 a 4 descrições, até 90 caracteres cada")
    url_final: str
    caminho1: str = ""
    caminho2: str = ""


class Grupo(BaseModel):
    nome: str
    cpc_maximo: Optional[float] = Field(None, description="Lance máximo do grupo em R$ (opcional)")
    palavras_chave: list[PalavraChave]
    anuncios: list[Anuncio]


class Lance(BaseModel):
    estrategia: Literal["maximizar_cliques", "maximizar_conversoes"] = "maximizar_cliques"
    cpc_maximo: Optional[float] = Field(None, description="Teto de CPC em R$ (só maximizar_cliques)")
    cpa_alvo: Optional[float] = Field(None, description="CPA desejado em R$ (só maximizar_conversoes, opcional)")


class PlanoCampanha(BaseModel):
    conta: Optional[str] = Field(None, description="ID da conta (com ou sem hífens); vazio = conta padrão da configuração")
    nome: str
    orcamento_diario: float = Field(description="Orçamento diário em R$")
    lance: Lance = Lance()
    locais: list[int] = Field([BRASIL], description="IDs de geoTargetConstants (2076 = Brasil)")
    idiomas: list[int] = Field([PORTUGUES], description="IDs de languageConstants (1014 = português)")
    parceiros_de_pesquisa: bool = False
    grupos: list[Grupo]
    negativas: list[PalavraChave] = Field([], description="Palavras-chave negativas no nível da campanha")


def limpar_conta(conta) -> str:
    return re.sub(r"\D", "", str(conta or ""))


def normalizar(plano: PlanoCampanha, conta_padrao: str | None) -> dict:
    d = plano.model_dump()
    d["conta"] = limpar_conta(d["conta"] or conta_padrao)
    d["nome"] = d["nome"].strip()
    return d


def codigo(plano: dict) -> str:
    """Código curto que identifica exatamente este plano (muda se qualquer detalhe mudar)."""
    bruto = json.dumps(plano, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(bruto.encode()).hexdigest()[:10]


def validar(plano: dict, orcamento_maximo: float | None = None) -> tuple[list[str], list[str]]:
    rep = editor.Report()
    erros, avisos = [], []

    if len(plano["conta"]) != 10:
        erros.append("Conta ausente ou inválida: informe 'conta' ou configure 'conta_padrao'.")
    if not plano["nome"]:
        erros.append("Campanha sem nome.")
    if plano["orcamento_diario"] <= 0:
        erros.append("Orçamento diário precisa ser maior que zero.")
    if orcamento_maximo is not None and plano["orcamento_diario"] > orcamento_maximo:
        erros.append(f"Orçamento de {_reais(plano['orcamento_diario'])}/dia passa do limite configurado "
                     f"({_reais(orcamento_maximo)}/dia).")

    lance = plano["lance"]
    if lance["estrategia"] == "maximizar_cliques" and lance["cpa_alvo"] is not None:
        erros.append("cpa_alvo só vale com maximizar_conversoes.")
    if lance["estrategia"] == "maximizar_conversoes":
        if lance["cpc_maximo"] is not None:
            erros.append("cpc_maximo só vale com maximizar_cliques.")
        avisos.append("Maximizar conversões depende da conversão estar medindo certo; sem histórico, o gasto oscila.")
    if not plano["locais"]:
        erros.append("Informe pelo menos um local.")
    if not plano["idiomas"]:
        erros.append("Informe pelo menos um idioma.")
    if not plano["grupos"]:
        erros.append("A campanha precisa de pelo menos um grupo de anúncios.")

    nomes = [g["nome"].strip().lower() for g in plano["grupos"]]
    if len(set(nomes)) < len(nomes):
        erros.append("Há grupos com o mesmo nome.")

    for g in plano["grupos"]:
        onde = f"Grupo {g['nome']!r}"
        if not g["palavras_chave"]:
            erros.append(f"{onde} sem palavras-chave.")
        elif len(g["palavras_chave"]) > 30:
            avisos.append(f"{onde} com {len(g['palavras_chave'])} palavras-chave; considere dividir.")
        if not g["anuncios"]:
            erros.append(f"{onde} sem anúncio.")
        for kw in g["palavras_chave"]:
            erros += _checar_palavra(onde, kw["texto"])
        for i, a in enumerate(g["anuncios"], 1):
            linha = {f"Headline {n}": t for n, t in enumerate(a["titulos"], 1)}
            linha.update({f"Description {n}": t for n, t in enumerate(a["descricoes"], 1)})
            linha.update({"Path 1": a["caminho1"], "Path 2": a["caminho2"], "Final URL": a["url_final"]})
            if len(a["titulos"]) > 15:
                rep.error(f"{onde}, anúncio {i}", f"{len(a['titulos'])} títulos (máx. 15)")
            if len(a["descricoes"]) > 4:
                rep.error(f"{onde}, anúncio {i}", f"{len(a['descricoes'])} descrições (máx. 4)")
            editor.check_rsa(rep, f"{onde}, anúncio {i}", linha)

    for neg in plano["negativas"]:
        erros += _checar_palavra("Negativa", neg["texto"])
        tipo = MATCH[neg["correspondencia"]].lower()
        for g in plano["grupos"]:
            for kw in g["palavras_chave"]:
                if _bloqueia(neg["texto"], tipo, kw["texto"]):
                    erros.append(f"Negativa {neg['texto']!r} ({neg['correspondencia']}) bloqueia a palavra-chave "
                                 f"{kw['texto']!r} do grupo {g['nome']!r}.")

    erros += [f"{e['row']}: {e['msg']}" for e in rep.errors]
    avisos += [f"{w['row']}: {w['msg']}" for w in rep.warnings]
    return erros, avisos


def _checar_palavra(onde: str, texto: str) -> list[str]:
    t = texto.strip()
    if not t:
        return [f"{onde}: palavra-chave vazia."]
    erros = []
    if len(t) > editor.KEYWORD_MAX_CHARS:
        erros.append(f"{onde}: {t!r} passa de {editor.KEYWORD_MAX_CHARS} caracteres.")
    if len(t.split()) > editor.KEYWORD_MAX_WORDS:
        erros.append(f"{onde}: {t!r} passa de {editor.KEYWORD_MAX_WORDS} palavras.")
    if not editor.KEYWORD_ALLOWED.match(t):
        erros.append(f"{onde}: {t!r} tem símbolo não permitido (use só letras, números, - & . ').")
    return erros


def _bloqueia(neg: str, tipo: str, pos: str) -> bool:
    n, p = neg.lower().split(), pos.lower().split()
    if tipo == "exact":
        return n == p
    if tipo == "phrase":
        return any(p[j:j + len(n)] == n for j in range(len(p) - len(n) + 1))
    return set(n) <= set(p)


def _reais(v: float) -> str:
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def resumo(plano: dict) -> str:
    lance = plano["lance"]
    if lance["estrategia"] == "maximizar_cliques":
        txt_lance = "Maximizar cliques" + (f", CPC máx. {_reais(lance['cpc_maximo'])}" if lance["cpc_maximo"] else "")
    else:
        txt_lance = "Maximizar conversões" + (f", CPA desejado {_reais(lance['cpa_alvo'])}" if lance["cpa_alvo"] else "")
    linhas = [
        f"Conta {plano['conta']} — campanha de Pesquisa **{plano['nome']}** (nasce PAUSADA)",
        f"- Orçamento: {_reais(plano['orcamento_diario'])}/dia (≈ {_reais(plano['orcamento_diario'] * 30.4)}/mês)",
        f"- Lance: {txt_lance}",
        f"- Locais: {', '.join(map(str, plano['locais']))} · Idiomas: {', '.join(map(str, plano['idiomas']))}"
        f" · Parceiros de pesquisa: {'sim' if plano['parceiros_de_pesquisa'] else 'não'}",
    ]
    for g in plano["grupos"]:
        kws = ", ".join(f"{k['texto']} ({k['correspondencia'].lower()})" for k in g["palavras_chave"])
        cpc = f", CPC {_reais(g['cpc_maximo'])}" if g["cpc_maximo"] else ""
        linhas.append(f"- Grupo **{g['nome']}**{cpc}: {len(g['palavras_chave'])} palavras-chave, "
                      f"{len(g['anuncios'])} anúncio(s) → {kws}")
        for a in g["anuncios"]:
            linhas.append(f"  - RSA {len(a['titulos'])} títulos / {len(a['descricoes'])} descrições → {a['url_final']}")
    if plano["negativas"]:
        linhas.append("- Negativas: " + ", ".join(f"{n['texto']} ({n['correspondencia'].lower()})"
                                                  for n in plano["negativas"]))
    return "\n".join(linhas)
