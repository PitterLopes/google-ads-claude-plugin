"""Transforma um plano validado em operações de mutate da API do Google Ads.

Tudo vai num único GoogleAdsService.mutate (atômico): ou cria tudo, ou nada.
Recursos novos usam IDs temporários negativos para se referenciarem na mesma chamada.
A campanha é SEMPRE criada pausada: não existe parâmetro para mudar isso.
"""
from plano import MATCH


def _micros(reais: float) -> int:
    # A API exige múltiplos de 10.000 micros (R$ 0,01)
    return int(round(reais * 100)) * 10_000


def montar(client, plano: dict) -> tuple[list, list[str]]:
    """Devolve (operações, rótulos); rótulos[i] descreve a operação i para mensagens de erro."""
    cid = plano["conta"]
    enums = client.enums
    ops, rotulos = [], []
    proximo = iter(range(-1, -100_000, -1))

    def nova(rotulo):
        op = client.get_type("MutateOperation")
        ops.append(op)
        rotulos.append(rotulo)
        return op

    orc_rn = f"customers/{cid}/campaignBudgets/{next(proximo)}"
    op = nova("orçamento")
    b = op.campaign_budget_operation.create
    b.resource_name = orc_rn
    b.name = f"{plano['nome']} - orçamento"
    b.amount_micros = _micros(plano["orcamento_diario"])
    b.delivery_method = enums.BudgetDeliveryMethodEnum.STANDARD
    b.explicitly_shared = False

    camp_rn = f"customers/{cid}/campaigns/{next(proximo)}"
    op = nova("campanha")
    c = op.campaign_operation.create
    c.resource_name = camp_rn
    c.name = plano["nome"]
    c.status = enums.CampaignStatusEnum.PAUSED
    c.advertising_channel_type = enums.AdvertisingChannelTypeEnum.SEARCH
    c.campaign_budget = orc_rn
    c.contains_eu_political_advertising = (
        enums.EuPoliticalAdvertisingStatusEnum.DOES_NOT_CONTAIN_EU_POLITICAL_ADVERTISING)
    c.network_settings.target_google_search = True
    c.network_settings.target_search_network = plano["parceiros_de_pesquisa"]
    c.network_settings.target_content_network = False
    c.network_settings.target_partner_search_network = False
    c.geo_target_type_setting.positive_geo_target_type = enums.PositiveGeoTargetTypeEnum.PRESENCE
    lance = plano["lance"]
    if lance["estrategia"] == "maximizar_cliques":
        client.copy_from(c.target_spend, client.get_type("TargetSpend"))
        if lance["cpc_maximo"]:
            c.target_spend.cpc_bid_ceiling_micros = _micros(lance["cpc_maximo"])
    else:
        client.copy_from(c.maximize_conversions, client.get_type("MaximizeConversions"))
        if lance["cpa_alvo"]:
            c.maximize_conversions.target_cpa_micros = _micros(lance["cpa_alvo"])

    for loc in plano["locais"]:
        cc = nova(f"local {loc}").campaign_criterion_operation.create
        cc.campaign = camp_rn
        cc.location.geo_target_constant = f"geoTargetConstants/{loc}"
    for idioma in plano["idiomas"]:
        cc = nova(f"idioma {idioma}").campaign_criterion_operation.create
        cc.campaign = camp_rn
        cc.language.language_constant = f"languageConstants/{idioma}"
    for neg in plano["negativas"]:
        cc = nova(f"negativa {neg['texto']!r}").campaign_criterion_operation.create
        cc.campaign = camp_rn
        cc.negative = True
        cc.keyword.text = neg["texto"].strip()
        cc.keyword.match_type = getattr(enums.KeywordMatchTypeEnum, MATCH[neg["correspondencia"]])

    for g in plano["grupos"]:
        grupo_rn = f"customers/{cid}/adGroups/{next(proximo)}"
        ag = nova(f"grupo {g['nome']!r}").ad_group_operation.create
        ag.resource_name = grupo_rn
        ag.name = g["nome"].strip()
        ag.campaign = camp_rn
        ag.status = enums.AdGroupStatusEnum.ENABLED
        ag.type_ = enums.AdGroupTypeEnum.SEARCH_STANDARD
        if g["cpc_maximo"]:
            ag.cpc_bid_micros = _micros(g["cpc_maximo"])

        for kw in g["palavras_chave"]:
            k = nova(f"palavra-chave {kw['texto']!r} em {g['nome']!r}").ad_group_criterion_operation.create
            k.ad_group = grupo_rn
            k.status = enums.AdGroupCriterionStatusEnum.ENABLED
            k.keyword.text = kw["texto"].strip()
            k.keyword.match_type = getattr(enums.KeywordMatchTypeEnum, MATCH[kw["correspondencia"]])

        for i, a in enumerate(g["anuncios"], 1):
            aga = nova(f"anúncio {i} em {g['nome']!r}").ad_group_ad_operation.create
            aga.ad_group = grupo_rn
            aga.status = enums.AdGroupAdStatusEnum.ENABLED
            aga.ad.final_urls.append(a["url_final"].strip())
            rsa = aga.ad.responsive_search_ad
            for t in a["titulos"]:
                asset = client.get_type("AdTextAsset")
                asset.text = t.strip()
                rsa.headlines.append(asset)
            for t in a["descricoes"]:
                asset = client.get_type("AdTextAsset")
                asset.text = t.strip()
                rsa.descriptions.append(asset)
            if a["caminho1"]:
                rsa.path1 = a["caminho1"].strip()
            if a["caminho2"]:
                rsa.path2 = a["caminho2"].strip()

    return ops, rotulos
