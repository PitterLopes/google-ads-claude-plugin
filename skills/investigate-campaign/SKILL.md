---
name: investigate-campaign
description: Investiga a causa de uma mudança de desempenho em uma campanha do Google Ads (queda de conversões, CPA subindo, gasto disparando, impressões sumindo) seguindo uma árvore de diagnóstico com dados. Use quando o usuário perguntar "o que aconteceu com a campanha X", "por que caiu" ou "por que está caro".
argument-hint: "[nome da campanha] [período]"
---

# Investigar campanha

Aplique `account-conventions` e a árvore de `performance-analysis`.

1. **Delimite**: campanha, métrica que mudou, quando começou. Compare janela "depois" × "antes" de mesmo tamanho.
2. **Série diária** (GAQL "série diária") — localize o dia da quebra. Mudança em degrau = evento (alteração, reprovação,
   rastreamento); mudança gradual = mercado/concorrência/sazonalidade.
3. **Rastreamento primeiro**: as outras campanhas também perderam conversões no mesmo dia? Se sim, suspeite da tag
   e pare aqui recomendando checar a conversão.
4. **Decomponha** (Custo = Impr × CTR × CPC; CPA = CPC ÷ Taxa conv.) e mostre qual fator explica a variação.
5. **Investigue o fator**:
   - Impressões → IS perdida por orçamento/classificação, palavras-chave pausadas/reprovadas, negativas novas.
   - CTR → anúncios reprovados/alterados, posição, termos de pesquisa novos.
   - CPC → leilão (Insights de leilão), mudança de meta de lance.
   - Taxa de conversão → termos de pesquisa novos, dispositivo, landing page (leia a URL), horário.
6. **Histórico de alterações** do período (GAQL `change_event`): cruze datas de mudanças com o dia da quebra.
7. **Conclusão**: causa mais provável com evidência numérica e grau de confiança; causas descartadas e por quê;
   ações recomendadas em ordem de impacto. Nada é alterado sem "ok".

Se faltar dado para concluir, diga exatamente qual export/consulta resolveria.
