---
name: account-conventions
description: Regras da casa para qualquer trabalho em Google Ads - contexto da conta, nomenclatura de campanhas, estrutura, como obter dados (MCP, API ou CSV exportado) e regras de segurança antes de alterar algo. Use sempre antes de criar, analisar ou mudar campanhas do Google Ads.
---

# Convenções da conta Google Ads

Todas as outras skills deste plugin partem daqui. Leia antes de agir.

## 1. Contexto da conta

Procure, nesta ordem, um arquivo de contexto do anunciante:

1. `google-ads-context.md` na pasta de trabalho atual
2. `.google-ads-context.local.md` na pasta de trabalho atual

Se não existir, ofereça criá-lo a partir de `references/context-template.md` e faça as perguntas mínimas
(negócio, oferta, público, região, meta de conversão, CPA/ROAS alvo, orçamento mensal). Não invente esses números:
sem eles, diga quais análises ficam limitadas.

O contexto vale mais que qualquer regra genérica deste plugin. Se ele disser "orçamento fixo" ou
"nunca pausar campanha de marca", isso manda.

## 2. Regras de segurança (inegociáveis)

- **Nada muda na conta sem um "ok" explícito do usuário**, item a item. Mostre antes: o que muda, valor atual → valor novo, impacto esperado.
- Campanhas novas sobem **pausadas**. Quem ativa é o usuário.
- Nunca aumente orçamento total da conta por conta própria; redistribuir dentro do mesmo total é proposta, não ação.
- Prefira gerar arquivo para o Google Ads Editor (o usuário revisa e publica) a escrever direto pela API.
- Não remova/exclua entidades: pause. Exclusão só se o usuário pedir com essas palavras.
- Registre toda mudança aplicada em `google-ads-changelog.md` (data, entidade, antes, depois, motivo).

## 3. Como obter dados

Use a primeira fonte disponível e diga ao usuário qual usou:

| Fonte | Como reconhecer | Lê | Escreve |
|---|---|---|---|
| MCP oficial do Google Ads (`googleads/google-ads-mcp`) | ferramentas `search` / `list_accessible_customers` | sim (GAQL) | não |
| Windsor.ai ou outro conector com Google Ads | ferramentas `get_data`, `execute_action` (`google_ads`) | sim | sim, com confirmação |
| CSV/planilha exportada pela interface do Google Ads | arquivo enviado pelo usuário | sim | não |
| Nenhuma | — | peça um export (veja abaixo) | gere arquivo do Editor |

Consultas GAQL prontas estão em `references/gaql-queries.md`. Ao usar conectores, descubra as ações e campos
disponíveis antes (ex.: `list_actions`, `get_fields`) em vez de supor que existem.

Sem conector, peça exports específicos da interface (Relatórios → personalizado, ou cada aba → Download → CSV):
- Campanhas: últimos 30 dias, segmentado por dia se for investigar tendência
- Termos de pesquisa: últimos 30-90 dias, com custo, conversões e grupo de anúncios
- Anúncios: RSAs com títulos/descrições e "Força do anúncio"
- Palavras-chave: com Índice de qualidade e seus 3 componentes

## 4. Nomenclatura

Padrão (adapte se o contexto definir outro):

```
Campanha:  [Rede]_[Objetivo]_[Tema]_[Geo]        ex.: SRCH_LEAD_Marca_BR, SRCH_VENDA_Produto-X_SP, PMAX_VENDA_Catalogo_BR
Grupo:     [Tema]_[Intenção]                      ex.: Software-Gestao_Comercial, Concorrente-Y_Comparativo
```
Redes: `SRCH` (Pesquisa), `PMAX`, `DISP` (Display), `VID` (YouTube), `DG` (Demand Gen).

## 5. Estrutura padrão para Pesquisa

- Separe **Marca** de **Não-marca** sempre (métricas e lances muito diferentes).
- Concorrentes em campanha própria, se forem usados.
- 1 tema de intenção por grupo; 5-20 palavras-chave por grupo; 1-2 RSAs por grupo.
- Correspondência: comece com Frase + Exata; Ampla só com lances inteligentes e conversões confiáveis (≥30/mês na campanha).
- Lance inicial: Maximizar cliques com teto de CPC ou Maximizar conversões quando já houver histórico; CPA/ROAS desejado só após ~30 conversões em 30 dias.
- Lista de negativas compartilhada da conta (emprego, grátis, curso, download, etc. conforme o negócio).

## 6. Moeda, idioma e números

- Use a moeda da conta. No Brasil: R$, vírgula decimal na conversa; ponto decimal nos arquivos CSV.
- A API trabalha em micros (1 R$ = 1.000.000 micros). Converta antes de mostrar.
- Sempre informe o período analisado e compare com o período anterior equivalente.
