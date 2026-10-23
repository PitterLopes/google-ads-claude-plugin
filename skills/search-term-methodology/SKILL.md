---
name: search-term-methodology
description: Metodologia para classificar termos de pesquisa do Google Ads - intenção, relevância, critérios de negativação, tipos de correspondência de negativas, níveis (grupo, campanha, lista) e promoção de termos a palavras-chave. Use ao analisar relatórios de termos de pesquisa ou montar listas de palavras-chave negativas.
---

# Metodologia de termos de pesquisa

## 1. Classifique cada termo em uma intenção

| Intenção | Sinais | Ação típica |
|---|---|---|
| Compra/contratação | preço, contratar, comprar, orçamento, "melhor X para", plano | manter / promover a palavra-chave |
| Comparação | vs, alternativa, comparativo, review | manter se houver página/argumento |
| Informacional | o que é, como fazer, exemplo, modelo, pdf | geralmente negativar em campanhas de conversão |
| Marca própria | nome da empresa/produto | garantir que está na campanha de Marca |
| Concorrente | marcas de terceiros | mover para campanha de concorrentes ou negativar |
| Irrelevante | outro produto, emprego, vaga, curso, grátis (se não oferece), outra cidade | negativar |
| Navegacional de terceiros | login, suporte, telefone de outra empresa | negativar |

## 2. Decida com dados, não só com intuição
- **Negativar por irrelevância**: pode ser imediato, mesmo com pouco gasto, se o termo é claramente fora do negócio.
- **Negativar por desempenho**: só após gastar ≥ 2-3× CPA alvo sem conversão (ou ROAS muito abaixo da meta com volume).
- **Promover a palavra-chave**: termo com ≥ 2 conversões e CPA ≤ meta, que ainda não existe como palavra-chave → adicione como Exata no grupo mais relevante.
- Termos com conversão mas fora da intenção do grupo → mova para o grupo certo (adicione lá e negative na origem como Exata).

## 3. Escolha a correspondência da negativa
- Negativa **Exata** `[termo]`: bloqueia só aquela busca. Use quando o termo parecido é bom.
- Negativa de **Frase** `"termo"`: bloqueia buscas que contêm a sequência. Padrão mais usado.
- Negativa **Ampla** `termo`: bloqueia buscas que contêm todas as palavras em qualquer ordem. Ótima para palavras únicas: `vaga`, `emprego`, `grátis`.
- Negativas **não** cobrem variações próximas (plural, erro de digitação): inclua as variações relevantes.
- Prefira **raízes de uma palavra** ("vaga", "curso", "pdf") a listar centenas de termos completos.

## 4. Escolha o nível
- **Lista compartilhada da conta**: lixo universal (emprego, curso, grátis, reclame aqui…).
- **Campanha**: termos que não servem àquela campanha (ex.: marca negativada na campanha Não-marca).
- **Grupo de anúncios**: para direcionar tráfego entre grupos (afunilamento), sempre Exata.

## 5. Antes de negativar, verifique conflitos
Uma negativa não pode bloquear uma palavra-chave ativa. Para cada negativa proposta, confira se alguma
palavra-chave positiva da mesma campanha contém aquela sequência. Se sim, reduza para Exata ou descarte.

## 6. Saída padrão
Tabela com: termo · campanha/grupo · cliques · custo · conversões · intenção · ação (negativar/promover/mover/manter)
· correspondência · nível · motivo. Agrupe negativas por raiz e mostre o **custo desperdiçado total** que elas
teriam evitado no período.
