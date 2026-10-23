# Google Ads para o Claude

Plugin com 10 skills que transformam o Claude em um gestor de Google Ads: cria campanhas de Pesquisa completas,
audita anúncios, minera termos de pesquisa, redistribui orçamento, investiga quedas e faz a revisão semanal.

Funciona **com ou sem acesso à API**: sem conector, ele trabalha com CSVs exportados da interface e entrega
arquivos prontos para o **Google Ads Editor**. Com conector, lê os dados direto da conta.
Nada é alterado na conta sem a sua confirmação, e campanhas novas sobem **pausadas**.

## Skills

| Skill | Tipo | O que faz |
|---|---|---|
| `account-conventions` | conhecimento | Contexto do anunciante, regras de segurança, nomenclatura, estrutura, fontes de dados e GAQL prontas |
| `ad-copy-principles` | conhecimento | Limites e políticas de RSA/extensões, fórmula dos 15 títulos |
| `performance-analysis` | conhecimento | Decomposição de métricas, árvore de diagnóstico, volume mínimo para concluir |
| `search-term-methodology` | conhecimento | Intenção de busca, critérios de negativação, correspondência e nível das negativas |
| `create-campaign` | ação | Briefing → grupos → palavras-chave → RSAs → negativas → extensões → **CSV validado** para o Editor |
| `audit-ad-copy` | ação | Nota de 0 a 16 por anúncio e reescritas prontas |
| `budget-optimize` | ação | Redistribui verba por eficiência e parcela de impressões perdida, com o total fixo |
| `investigate-campaign` | ação | "Por que caiu?" com série diária, decomposição e histórico de alterações |
| `mine-search-terms` | ação | Desperdício por raiz, negativas sem conflito, novas palavras-chave |
| `weekly-review` | ação | Placar da semana × meta, alertas e 5 ações priorizadas |

As skills de conhecimento são usadas automaticamente pelas de ação. Você pode chamar uma de ação pelo nome
(ex.: `/google-ads:create-campaign`) ou só pedir em linguagem natural: *"cria uma campanha de pesquisa para
implante dentário em SP com R$ 80/dia"*.

## Instalação

### Claude Code
```bash
/plugin marketplace add PitterLopes/google-ads-claude-plugin
/plugin install google-ads@google-ads-claude
```

### App do Claude (desktop / claude.ai)
Adicione pelo gerenciador de plugins do app (aba de plugins/personalizar), apontando para este repositório
ou enviando o `.zip` gerado por `./build-zip.sh`. Se o seu plano só aceitar skills avulsas, envie cada pasta
de `skills/` compactada.

## Conectando à sua conta (opcional)

O plugin detecta a fonte disponível e diz qual usou:

1. **MCP oficial do Google Ads** — [googleads/google-ads-mcp](https://github.com/googleads/google-ads-mcp).
   Somente leitura, consultas GAQL. Precisa de developer token da API do Google Ads e credenciais do Google Cloud;
   siga o README do repositório.
2. **Conectores de terceiros** (ex.: Windsor.ai) — leitura e, em alguns, escrita (orçamento, status, palavras-chave).
   Toda escrita passa por confirmação.
3. **Sem conector** — exporte relatórios da interface (Campanhas, Termos de pesquisa, Anúncios, Palavras-chave) em CSV
   e envie para o Claude.

## Primeiro uso

1. Peça: *"configura o contexto do Google Ads"*. O Claude cria `google-ads-context.md` com seu negócio, metas
   de CPA/ROAS, orçamento e regras (modelo em `skills/account-conventions/references/context-template.md`).
2. Peça o que precisar: criar campanha, revisão semanal, minerar termos etc.
3. Mudanças aplicadas ficam registradas em `google-ads-changelog.md`.

## Validador do Google Ads Editor

`create-campaign` gera o CSV e roda um validador (Python, só biblioteca padrão) antes de entregar:

```bash
python3 skills/create-campaign/scripts/validate_editor_csv.py examples/exemplo-campanha.csv
```

Ele verifica limites de caracteres, quantidade de títulos/descrições, duplicados, `!` e emojis em títulos,
caminhos, URL final, formato de palavras-chave, campanha pausada, grupos sem anúncio e **negativas que bloqueiam
palavras-chave ativas**. Para importar: Google Ads Editor → Conta › Importar › De arquivo → revisar → Publicar.

## Segurança

- Nenhuma alteração sem "ok" explícito, item a item.
- Campanhas novas sobem pausadas; orçamento total não sobe sem autorização.
- Pausa em vez de excluir.

## Contribuindo

Issues e PRs são bem-vindos — especialmente novas skills (Performance Max, Shopping, YouTube), traduções e
melhorias no validador. Mantenha cada `SKILL.md` curto e objetivo: detalhes vão para `references/`.

## Licença

MIT
