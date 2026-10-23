# Formato do CSV para o Google Ads Editor

Um único arquivo, UTF-8, separado por vírgula, com o cabeçalho abaixo (nomes em inglês, exatamente assim —
o Editor reconhece esses nomes de coluna em qualquer idioma da interface). Cada linha é **um** tipo de entidade;
deixe as outras colunas vazias.

```
Campaign,Campaign Type,Networks,Budget,Budget type,Bid Strategy Type,Campaign Status,Languages,Location,Ad Group,Ad Group Status,Max CPC,Keyword,Criterion Type,Ad type,Headline 1,Headline 2,Headline 3,Headline 4,Headline 5,Headline 6,Headline 7,Headline 8,Headline 9,Headline 10,Headline 11,Headline 12,Headline 13,Headline 14,Headline 15,Description 1,Description 2,Description 3,Description 4,Path 1,Path 2,Final URL
```

## Tipos de linha

| Linha | Colunas preenchidas |
|---|---|
| Campanha | Campaign, Campaign Type=`Search`, Networks=`Google search`, Budget (diário, ponto decimal), Budget type=`Daily`, Bid Strategy Type (`Maximize clicks`, `Maximize conversions`, `Manual CPC`, `Target CPA`), Campaign Status=`Paused`, Languages (`pt`), Location (ex.: `Brazil`, `São Paulo, Brazil`) |
| Grupo | Campaign, Ad Group, Ad Group Status=`Enabled`, Max CPC (opcional) |
| Palavra-chave | Campaign, Ad Group, Keyword, Criterion Type=`Exact` / `Phrase` / `Broad` |
| Negativa de grupo | Campaign, Ad Group, Keyword, Criterion Type=`Negative Exact` / `Negative Phrase` / `Negative Broad` |
| Negativa de campanha | Campaign, Keyword, Criterion Type=`Campaign Negative Exact` / `Campaign Negative Phrase` / `Campaign Negative Broad` |
| RSA | Campaign, Ad Group, Ad type=`Responsive search ad`, Headline 1..15, Description 1..4, Path 1, Path 2, Final URL |

Palavras-chave vão **sem** colchetes/aspas na coluna Keyword; a correspondência fica em Criterion Type.

## Notas
- Se a localização não for reconhecida, o Editor marca a linha com erro na revisão — ajuste para o nome que ele sugerir.
- Linhas com o mesmo nome de campanha/grupo de uma entidade existente **atualizam** a existente. Use nomes novos para criar.
- Extensões (sitelinks, callouts) ficam fora deste CSV; adicione pela interface ou Editor (Recursos).
- Exemplo completo: `examples/exemplo-campanha.csv` na raiz do plugin.
