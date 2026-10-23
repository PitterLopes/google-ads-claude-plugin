---
name: ad-copy-principles
description: Princípios e limites técnicos para escrever anúncios do Google Ads - anúncios responsivos de pesquisa (RSA), sitelinks, frases de destaque, snippets estruturados e textos de PMax. Use ao escrever, reescrever ou revisar qualquer texto de anúncio do Google Ads.
---

# Princípios de texto para Google Ads

## Limites (o Google rejeita se passar)

| Elemento | Limite | Quantidade |
|---|---|---|
| Título RSA | 30 caracteres | 3 a 15 (mire 12-15) |
| Descrição RSA | 90 caracteres | 2 a 4 (mire 4) |
| Caminho 1 / 2 | 15 caracteres cada | opcional |
| Sitelink — texto | 25 | 2+ por campanha (mire 6-8) |
| Sitelink — linhas de descrição | 35 cada | 2 |
| Frase de destaque (callout) | 25 | mire 6-10 |
| Snippet estruturado — valor | 25 | 3-10 por cabeçalho |
| PMax — título curto / longo | 30 / 90 | até 15 / até 5 |
| PMax — descrição | 90 (uma de até 60) | até 5 |
| Nome da empresa | 25 | 1 |

Caracteres acentuados contam como 1. Símbolos de largura dupla (CJK) contam como 2.
`{KeyWord:texto padrão}` conta pelo texto padrão.

## Políticas que derrubam anúncio
- Sem pontuação repetida (`!!`, `??`), sem `!` em título, sem CAIXA ALTA gratuita ("GRÁTIS").
- Sem emojis e símbolos decorativos (★ ✓ →).
- Sem telefone no texto (use extensão de chamada).
- Sem frases genéricas de clique ("clique aqui").
- Afirmações superlativas ("o melhor", "nº 1") só com comprovação na landing page.
- Marcas de terceiros podem ser restritas em texto; não use marca de concorrente no anúncio.
- Saúde, finanças, jurídico e apostas têm regras extras: sinalize ao usuário.

## Como montar um RSA forte (15 títulos)

Distribua os títulos por função, para que qualquer combinação faça sentido sozinha:

| Função | Qtd | Exemplo (software de atendimento) |
|---|---|---|
| Palavra-chave / o que é | 3-4 | "Software de Atendimento" |
| Benefício concreto | 3-4 | "Responda 3x Mais Rápido" |
| Prova (número, cliente, prêmio) | 2-3 | "+2.000 Empresas Usam" |
| Oferta / redução de risco | 2 | "Teste Grátis por 14 Dias" |
| Chamada para ação | 2 | "Comece Hoje Mesmo" |
| Marca | 1 | "DropDesk Oficial" |

Regras:
- Cada título deve ser diferente em **ideia**, não só em palavras. O Google penaliza repetição ("Força do anúncio").
- Pelo menos 2-3 títulos contêm a palavra-chave principal do grupo (relevância → Índice de qualidade).
- Use números e especificidade: "Setup em 10 Minutos" > "Setup Rápido".
- Fale do resultado do cliente, não da sua empresa.
- Fixe (pin) só quando obrigatório (ex.: aviso legal). Fixar em excesso derruba a Força do anúncio.
- Title Case nos títulos é comum no Brasil e aceito; mantenha consistente.

Descrições (4):
1. Benefício principal + prova
2. Como funciona / o que inclui
3. Objeção resolvida (preço, contrato, suporte, prazo)
4. Oferta + CTA

## Alinhamento com a landing page
A promessa do anúncio deve aparecer acima da dobra da página de destino. Se o anúncio diz "Teste Grátis",
a página precisa ter o botão de teste grátis. Sinalize desalinhamentos.

## Extensões mínimas por campanha de Pesquisa
- 4+ sitelinks (com descrições), 4+ frases de destaque, 1 snippet estruturado, imagem e logotipo se elegível,
  chamada se o negócio atende por telefone, local se tem loja física.

## Checklist antes de entregar texto
- [ ] Todos os limites respeitados (rode o validador do `create-campaign` se gerar CSV)
- [ ] Nenhum título repetido ou quase repetido
- [ ] Palavra-chave do grupo em 2+ títulos
- [ ] Pelo menos 1 número/prova e 1 oferta
- [ ] Sem violações de política listadas acima
- [ ] Coerente com a landing page e com o tom do `google-ads-context.md`
