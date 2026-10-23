# Consultas GAQL prontas

Para uso com a ferramenta `consulta_gaql` do plugin, o MCP oficial do Google Ads (ferramenta `search`) ou qualquer cliente da API.
Troque `LAST_30_DAYS` por `DURING LAST_7_DAYS`, `LAST_14_DAYS` ou `segments.date BETWEEN 'AAAA-MM-DD' AND 'AAAA-MM-DD'`.
Valores `*_micros` ÷ 1.000.000 = moeda da conta.

## Campanhas — desempenho
```sql
SELECT campaign.id, campaign.name, campaign.status, campaign.advertising_channel_type,
       campaign.bidding_strategy_type, campaign_budget.amount_micros,
       metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions,
       metrics.conversions_value, metrics.search_impression_share,
       metrics.search_budget_lost_impression_share, metrics.search_rank_lost_impression_share
FROM campaign
WHERE segments.date DURING LAST_30_DAYS AND campaign.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
```

## Campanhas — série diária (investigar quedas)
```sql
SELECT segments.date, campaign.name, metrics.impressions, metrics.clicks,
       metrics.cost_micros, metrics.conversions, metrics.average_cpc
FROM campaign
WHERE segments.date DURING LAST_30_DAYS AND campaign.id = {CAMPAIGN_ID}
ORDER BY segments.date
```

## Grupos de anúncios
```sql
SELECT campaign.name, ad_group.id, ad_group.name, ad_group.status,
       metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
FROM ad_group
WHERE segments.date DURING LAST_30_DAYS AND ad_group.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
```

## Termos de pesquisa
```sql
SELECT search_term_view.search_term, search_term_view.status, campaign.name, ad_group.name,
       metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions,
       metrics.conversions_value
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
ORDER BY metrics.cost_micros DESC
LIMIT 1000
```

## Palavras-chave com Índice de qualidade
```sql
SELECT campaign.name, ad_group.name, ad_group_criterion.keyword.text,
       ad_group_criterion.keyword.match_type, ad_group_criterion.status,
       ad_group_criterion.quality_info.quality_score,
       ad_group_criterion.quality_info.creative_quality_score,
       ad_group_criterion.quality_info.post_click_quality_score,
       ad_group_criterion.quality_info.search_predicted_ctr,
       metrics.clicks, metrics.cost_micros, metrics.conversions
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS AND ad_group_criterion.status != 'REMOVED'
ORDER BY metrics.cost_micros DESC
```

## Anúncios RSA (textos e força)
```sql
SELECT campaign.name, ad_group.name, ad_group_ad.ad.id, ad_group_ad.status,
       ad_group_ad.ad_strength, ad_group_ad.ad.final_urls,
       ad_group_ad.ad.responsive_search_ad.headlines,
       ad_group_ad.ad.responsive_search_ad.descriptions,
       ad_group_ad.ad.responsive_search_ad.path1, ad_group_ad.ad.responsive_search_ad.path2,
       metrics.impressions, metrics.clicks, metrics.conversions, metrics.cost_micros
FROM ad_group_ad
WHERE ad_group_ad.ad.type = 'RESPONSIVE_SEARCH_AD' AND ad_group_ad.status != 'REMOVED'
  AND segments.date DURING LAST_30_DAYS
```

## Negativas existentes (campanha)
```sql
SELECT campaign.name, campaign_criterion.keyword.text, campaign_criterion.keyword.match_type
FROM campaign_criterion
WHERE campaign_criterion.negative = TRUE AND campaign_criterion.type = 'KEYWORD'
```

## Histórico de alterações (o que mudou?)
Janela máxima de 30 dias atrás; `LIMIT` é obrigatório nesse recurso.
```sql
SELECT change_event.change_date_time, change_event.user_email, change_event.change_resource_type,
       change_event.resource_change_operation, change_event.changed_fields, campaign.name
FROM change_event
WHERE change_event.change_date_time >= '{AAAA-MM-DD}' AND change_event.change_date_time <= '{AAAA-MM-DD}'
ORDER BY change_event.change_date_time DESC
LIMIT 200
```

## Contas acessíveis (MCC)
Use a ferramenta `list_accessible_customers` do MCP, ou:
```sql
SELECT customer_client.id, customer_client.descriptive_name, customer_client.currency_code
FROM customer_client WHERE customer_client.level <= 1
```
