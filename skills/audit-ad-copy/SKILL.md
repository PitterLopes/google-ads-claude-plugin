---
name: audit-ad-copy
description: Audita os anúncios RSA de uma conta ou campanha do Google Ads - limites, políticas, repetição, força do anúncio, uso de palavra-chave, provas e oferta - e propõe reescritas prontas. Use quando o usuário pedir para revisar, auditar ou melhorar anúncios do Google Ads.
argument-hint: "[campanha ou 'conta toda']"
---

# Auditoria de anúncios

Aplique `account-conventions` e `ad-copy-principles`.

1. **Colete**: RSAs ativos com títulos, descrições, caminhos, URL final, força do anúncio e métricas de 30 dias
   (GAQL "Anúncios RSA" em `account-conventions/references/gaql-queries.md`, conector, ou export do usuário).
   Pegue também as 5 palavras-chave de maior gasto de cada grupo.
2. **Pontue cada anúncio** (0-2 por critério, total /16):
   - Quantidade: 12-15 títulos e 4 descrições
   - Diversidade: sem títulos redundantes em ideia
   - Relevância: palavra-chave do grupo em 2+ títulos
   - Especificidade: números, prazos, provas
   - Oferta / redução de risco presente
   - CTA claro
   - Política e limites ok
   - Coerência com a landing page (leia a URL final se possível)
3. **Priorize** por gasto: anúncios que concentram verba e pontuam baixo primeiro.
4. **Reescreva**: para cada anúncio prioritário, entregue o conjunto novo completo (15 títulos / 4 descrições) com
   contagem de caracteres, marcando o que manter, trocar e adicionar. Não apague títulos que performam bem
   (se o conector fornecer desempenho por recurso, use "Melhor"/"Bom"/"Baixo").
5. **Saída**: tabela-resumo (campanha · grupo · gasto · força · nota · principal problema), depois as reescritas.
   Se o usuário quiser aplicar, gere o CSV no formato de `create-campaign/references/editor-csv-format.md`
   como **novo** anúncio no mesmo grupo (o antigo é pausado depois de o novo acumular dados), e valide com
   `create-campaign/scripts/validate_editor_csv.py`.

Nunca edite anúncios na conta sem confirmação explícita.
