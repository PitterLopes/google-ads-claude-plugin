---
name: mine-search-terms
description: Minera o relatório de termos de pesquisa do Google Ads para achar desperdício (negativas) e oportunidades (novas palavras-chave), com custo desperdiçado e lista pronta para aplicar. Use quando o usuário pedir negativas, limpeza de termos de pesquisa ou novas palavras-chave a partir do que já busca.
argument-hint: "[campanha] [período, padrão 30 dias]"
---

# Minerar termos de pesquisa

Aplique `account-conventions` e `search-term-methodology`.

1. **Colete** termos de pesquisa (GAQL "Termos de pesquisa", conector ou export), as palavras-chave ativas e as
   negativas existentes da(s) campanha(s). Período padrão: 30 dias (90 se o volume for baixo).
2. **Trate em lote**: agrupe termos por raiz/n-grama (1 e 2 palavras) e some custo, cliques e conversões por raiz.
   Raízes com muito gasto e zero conversão aparecem primeiro. Para muitos termos, faça isso com um script
   (pandas/csv) em vez de ler linha a linha.
3. **Classifique** cada termo/raiz pela tabela de intenção da metodologia.
4. **Monte três listas**:
   - **Negativas** (raiz · correspondência · nível · custo evitado · exemplos de termos bloqueados)
   - **Novas palavras-chave** (termo · grupo destino · correspondência · conversões · CPA)
   - **Revisar** (casos ambíguos para o usuário decidir)
5. **Cheque conflitos**: nenhuma negativa pode bloquear palavra-chave ativa.
6. **Entregue** o total de gasto desperdiçado no período e o CSV pronto para o Editor
   (formato `create-campaign/references/editor-csv-format.md`, `Campaign Negative ...` / `Negative ...` / palavras-chave
   novas), validado com `create-campaign/scripts/validate_editor_csv.py`.

Aplicar na conta só com confirmação explícita; registre em `google-ads-changelog.md`.
