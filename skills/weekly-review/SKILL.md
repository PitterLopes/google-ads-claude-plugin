---
name: weekly-review
description: Revisão semanal da conta do Google Ads - resultado da semana contra metas, o que mudou, alertas, termos de pesquisa novos, anúncios e lista priorizada de ações para a próxima semana. Use quando o usuário pedir revisão semanal, relatório da semana ou "como foi a semana nos anúncios".
argument-hint: "[semana, padrão: últimos 7 dias completos]"
---

# Revisão semanal

Aplique `account-conventions` e `performance-analysis`. Período: últimos 7 dias completos (seg-dom) × 7 dias anteriores,
e mês até agora × meta mensal.

## Roteiro
1. **Placar**: gasto, conversões, CPA/ROAS, valor — semana × anterior × meta. Ritmo do mês (gasto projetado vs orçamento).
2. **Por campanha**: tabela ordenada por gasto com variações; marque 🔴 (fora da meta com volume), 🟡 (atenção), 🟢.
3. **Alertas** (cheque cada um):
   - Conversões zeradas ou queda > 30% em campanha relevante (suspeite de rastreamento)
   - Gasto > 120% do ritmo planejado
   - Anúncios/palavras-chave reprovados ou limitados
   - IS perdida por orçamento > 20% em campanha eficiente
   - Estratégia de lance em aprendizado ou "limitada"
   - Mudanças feitas na semana (histórico de alterações) e efeito observado
4. **Termos de pesquisa** da semana: top 10 por gasto sem conversão → sugestões de negativas (método `search-term-methodology`).
5. **Ações da próxima semana**: no máximo 5, priorizadas por impacto em R$, cada uma com dono (usuário/Claude),
   esforço e se precisa de "ok". Inclua as revisões pendentes do `google-ads-changelog.md` (mudanças de 7-14 dias atrás).

## Saída
Salve `reports/revisao-AAAA-MM-DD.md` com o relatório e mostre o resumo de 5 linhas na conversa.
Se o usuário quiser rodar toda semana, sugira agendar (tarefa agendada / rotina) com este mesmo comando.
