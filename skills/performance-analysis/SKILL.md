---
name: performance-analysis
description: Método para ler métricas do Google Ads e diagnosticar causas - CPA, ROAS, CTR, CPC, taxa de conversão, parcela de impressões, Índice de qualidade, significância estatística e árvore de diagnóstico. Use ao interpretar resultados ou explicar por que uma campanha do Google Ads melhorou ou piorou.
---

# Análise de desempenho no Google Ads

## Métricas e o que elas respondem

| Pergunta | Métrica |
|---|---|
| Estou pagando caro por resultado? | CPA = custo ÷ conversões; ROAS = valor conv. ÷ custo |
| O anúncio atrai clique? | CTR = cliques ÷ impressões |
| O clique está caro? | CPC médio |
| A página converte? | Taxa de conversão = conversões ÷ cliques |
| Estou perdendo leilões? | Parcela de impr. de pesquisa (IS); IS perdida por orçamento; IS perdida por classificação |
| Qualidade/relevância | Índice de qualidade e componentes (CTR esperada, relevância do anúncio, experiência na página) |

Sempre compare com o período anterior equivalente (mesmo número de dias, mesmos dias da semana)
e, quando houver, com o mesmo período do ano anterior.

## Decomposição — sempre faça antes de concluir
```
Custo      = Impressões × CTR × CPC
Conversões = Impressões × CTR × Taxa de conversão
CPA        = CPC ÷ Taxa de conversão
```
Uma variação de CPA vem de CPC, de taxa de conversão ou dos dois. Diga qual, com números.

## Árvore de diagnóstico

**Conversões caíram**
1. Medição: a tag/conversão parou? (conversões zeradas de repente em todas as campanhas = suspeite de rastreamento antes de tudo)
2. Volume: impressões caíram? → IS perdida por orçamento (verba) ou por classificação (lance/qualidade); sazonalidade; termos pausados/negativados.
3. CTR caiu? → anúncio novo/reprovado, concorrente novo, posição pior, mudança nos termos que acionam.
4. Taxa de conversão caiu? → página (velocidade, formulário, oferta), tráfego menos qualificado (termos de pesquisa), dispositivo/horário.
5. Houve mudança na conta? → consulte o histórico de alterações (lance, orçamento, estratégia, anúncios).
6. Estratégia de lance em aprendizado? → mudanças grandes (>20-30% de meta ou orçamento) reiniciam o aprendizado por ~1-2 semanas.

**CPA subiu**
- CPC subiu → leilão mais competitivo (veja Insights de leilão), meta de CPA/ROAS alterada, IS perdida por classificação.
- Taxa de conversão caiu → item 4 acima.

## Volume mínimo antes de concluir (evite agir sobre ruído)
- Palavra-chave/termo sem conversão: só considere ruim após gastar **≥ 2-3× o CPA alvo** ou ~100 cliques.
- Comparar taxas (CTR, taxa de conversão) entre dois anúncios/grupos: use teste de proporções; com < 30 conversões por lado, trate como indício, não conclusão.
- Dias isolados não são tendência. Mínimo 7 dias, ideal 14-30.
- Atraso de conversão: os últimos 3-7 dias costumam estar subnotificados (ciclos longos: mais). Avise.

## Benchmarks de referência (Pesquisa, só como sanity check)
CTR 3-8% em não-marca, 15-40% em marca. Taxa de conversão 2-10% conforme nicho.
Índice de qualidade ≤ 4 merece atenção; ≥ 7 é saudável. Use as metas do `google-ads-context.md` acima de qualquer benchmark.

## Formato de saída
1. **Resumo em 3 linhas**: o que aconteceu, por quê (com número), o que fazer.
2. Tabela com métricas atual × anterior × variação.
3. Causas ordenadas por impacto em R$.
4. Ações recomendadas com impacto estimado e nível de confiança (alta/média/baixa).
