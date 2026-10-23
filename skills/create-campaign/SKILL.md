---
name: create-campaign
description: Cria uma campanha de Pesquisa do Google Ads completa a partir de um briefing - pesquisa de intenção, estrutura de grupos, palavras-chave, anúncios RSA, negativas e extensões - e entrega um CSV validado para importar no Google Ads Editor (ou publica via conector, pausada, após confirmação). Use quando o usuário pedir para criar, montar, estruturar ou lançar uma campanha no Google Ads.
argument-hint: "[produto ou landing page] [orçamento diário] [região]"
---

# Criar campanha de Pesquisa no Google Ads

Antes de começar, aplique `account-conventions` (contexto, segurança, nomenclatura) e, ao escrever anúncios,
`ad-copy-principles`.

## Passo 1 — Briefing (pergunte só o que faltar no contexto)
Necessário: produto/oferta, URL da landing page, região, idioma, orçamento diário, conversão medida,
CPA alvo (ou valor da venda), se é Marca ou Não-marca. Se houver URL, leia a página para extrair
benefícios, provas, oferta e termos que o cliente usa.

Se a conta tiver dados (MCP/conector/CSV), consulte antes: termos de pesquisa que já convertem, negativas
existentes e campanhas que possam canibalizar a nova.

## Passo 2 — Mapa de intenção → grupos
Liste as intenções de busca de quem compraria (problema, solução, categoria, comparação, local, preço).
Cada intenção forte vira um grupo. Mostre ao usuário uma tabela:

| Grupo | Intenção | Palavras-chave exemplo | Landing page |
|---|---|---|---|

Mire 3-7 grupos para começar. Pouca verba (< R$ 50/dia) → 2-3 grupos, só os de maior intenção.

## Passo 3 — Palavras-chave
- 5-20 por grupo, todas da mesma intenção. Frase + Exata por padrão (veja `account-conventions` §5).
- Máximo 80 caracteres e 10 palavras por palavra-chave; sem símbolos além de `-`, `&`, `.`, `'`.
- Se houver ferramenta de volume (Planejador de palavras-chave via conector), use para priorizar; senão, sinalize que os volumes não foram verificados.

## Passo 4 — Anúncios
1 RSA por grupo (2 se houver hipótese clara para testar), 15 títulos e 4 descrições seguindo `ad-copy-principles`.
Título com a palavra-chave principal do grupo em pelo menos 2 posições. Caminhos (Path 1/2) com a palavra-chave.

## Passo 5 — Negativas
- Nível campanha: termos irrelevantes óbvios do nicho + marca própria (se for Não-marca).
- Sugira uma lista compartilhada da conta se não existir (vaga, emprego, curso, grátis, pdf, download, reclame aqui…, adaptado ao negócio).
- Confira conflitos com as palavras-chave positivas (o validador faz isso).

## Passo 6 — Extensões
Escreva 4-8 sitelinks (texto + 2 descrições + URL), 6-10 frases de destaque e 1 snippet estruturado.
Entregue-os no plano (passo 8); o usuário adiciona no Editor/interface, ou você publica via conector se houver.

## Passo 7 — Gerar e validar o CSV
Gere `out/<NomeDaCampanha>.csv` no formato de `references/editor-csv-format.md` (UTF-8, vírgula, cabeçalho exato).
A campanha **sempre** com `Campaign Status = Paused`.

Rode o validador e corrija até zerar os erros:
```bash
python3 <pasta-desta-skill>/scripts/validate_editor_csv.py out/<NomeDaCampanha>.csv
```
(`<pasta-desta-skill>` é o diretório onde este SKILL.md está.) Avisos (warnings) podem ficar, mas explique-os.

## Passo 8 — Entregar
Salve também `out/<NomeDaCampanha>-plano.md` com: resumo da estratégia, tabela de grupos, orçamento e lance,
negativas, extensões, o que medir na primeira e segunda semana e critérios para mudar o lance
(ex.: "trocar para CPA desejado após 30 conversões").

Diga ao usuário como importar:
1. Google Ads Editor → baixar a conta → **Conta › Importar › De arquivo** → escolha o CSV
2. Revise as alterações pendentes → **Publicar**
3. A campanha sobe pausada; ative quando revisar extensões e conversões.

## Publicação direta (opcional)
Só se houver conector com escrita no Google Ads (ex.: Windsor.ai `execute_action` com `google_ads`) **e** o
usuário confirmar explicitamente depois de ver o plano. Descubra as ações disponíveis antes (`list_actions`),
crie tudo pausado, registre em `google-ads-changelog.md` e informe os IDs criados.

## Variações
- **Performance Max**: em vez de palavras-chave, entregue grupo de recursos (15 títulos curtos, 5 longos, 5 descrições,
  sinais de público, temas de pesquisa) em markdown; o CSV do Editor não cobre bem imagens/vídeos.
- **Campanha de Marca**: 1 grupo, Exata + Frase da marca e variações/erros de digitação, CPC baixo, IS alvo.
