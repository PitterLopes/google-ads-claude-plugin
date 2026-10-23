---
name: budget-optimize
description: Redistribui o orçamento entre campanhas do Google Ads com base em CPA/ROAS marginal, parcela de impressões perdida por orçamento e metas, mantendo o total fixo salvo autorização. Use quando o usuário perguntar onde colocar mais ou menos verba, como dividir o orçamento ou se alguma campanha está limitada.
argument-hint: "[orçamento total, se mudar]"
---

# Otimização de orçamento

Aplique `account-conventions` (regra: o total não sobe sem autorização) e `performance-analysis`.

1. **Dados (30 dias + 30 anteriores)** por campanha: orçamento diário, gasto, conversões, valor, CPA, ROAS,
   IS de pesquisa, IS perdida por orçamento, IS perdida por classificação, estratégia de lance e status de aprendizado.
2. **Classifique cada campanha**:
   | Situação | Sinal | Direção |
   |---|---|---|
   | Eficiente e limitada | CPA ≤ meta e IS perdida por orçamento > 10% | receber verba |
   | Eficiente e saturada | CPA ≤ meta, IS perdida por orçamento ≈ 0 | manter (mais verba não compra mais) |
   | Ineficiente | CPA > 1,3× meta com volume suficiente | tirar verba / corrigir antes |
   | Sem dados | < 2× CPA alvo gasto | manter, aguardar |
   | Marca | — | manter IS alta; verba costuma ser pequena |
3. **Estime o retorno marginal**: verba extra em campanha limitada por orçamento rende ~ ao CPA atual até a IS
   perdida zerar; acima disso o CPA sobe. Seja conservador e diga que é estimativa.
4. **Proposta**: tabela campanha · orçamento atual → novo · Δ · motivo · conversões esperadas. Soma igual ao total atual.
   - Mudanças de no máximo ±20-30% por campanha por vez (evita reiniciar aprendizado do lance inteligente).
   - Se a campanha é limitada por **classificação** e não por orçamento, mais verba não resolve: aponte lance/qualidade.
5. **Aplicar**: só com "ok" explícito. Via conector com escrita ou instruções passo a passo para a interface/Editor.
   Registre em `google-ads-changelog.md` e sugira data de revisão (7-14 dias).
