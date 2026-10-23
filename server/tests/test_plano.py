"""Testes sem rede: validação, código de confirmação e montagem das operações.

Rodar: <venv>/bin/python -m unittest discover -s server/tests
"""
import copy
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from google.ads.googleads.client import GoogleAdsClient  # noqa: E402
from google.auth.credentials import AnonymousCredentials  # noqa: E402

import operacoes  # noqa: E402
from plano import PlanoCampanha, codigo, normalizar, validar  # noqa: E402

TITULOS = ["Sistema de atendimento", "WhatsApp com vários atendentes", "Teste grátis por 7 dias",
           "Atenda pelo mesmo número", "Relatórios de atendimento", "Chatbot e filas no WhatsApp",
           "Para escritórios contábeis", "Organize seu atendimento", "Histórico de conversas",
           "Implantação acompanhada"]
DESCRICOES = ["Vários atendentes no mesmo número de WhatsApp, com filas e histórico.",
              "Organize o atendimento do seu escritório e acompanhe tudo em relatórios.",
              "Teste o sistema e veja como funciona na sua rotina.",
              "Suporte em português e implantação acompanhada pela nossa equipe."]


def plano_base(**mudancas):
    d = {
        "nome": "SRCH_LEAD_WhatsApp-Atendentes_BR",
        "orcamento_diario": 50,
        "lance": {"estrategia": "maximizar_cliques", "cpc_maximo": 4.5},
        "grupos": [{
            "nome": "WhatsApp-Atendentes_Solucao",
            "palavras_chave": [{"texto": "whatsapp com varios atendentes"},
                               {"texto": "sistema de atendimento whatsapp", "correspondencia": "EXATA"}],
            "anuncios": [{"titulos": TITULOS, "descricoes": DESCRICOES,
                          "url_final": "https://www.example.com/", "caminho1": "whatsapp", "caminho2": "atendentes"}],
        }],
        "negativas": [{"texto": "gratis"}, {"texto": "vaga"}],
    }
    d.update(mudancas)
    return PlanoCampanha(**d)


class TestPlano(unittest.TestCase):
    def test_plano_valido(self):
        d = normalizar(plano_base(), "123-456-7890")
        erros, _ = validar(d)
        self.assertEqual(erros, [])
        self.assertEqual(d["conta"], "1234567890")

    def test_codigo_muda_com_qualquer_detalhe(self):
        a = normalizar(plano_base(), "1234567890")
        b = copy.deepcopy(a)
        self.assertEqual(codigo(a), codigo(b))
        b["grupos"][0]["anuncios"][0]["titulos"][0] = "Outro título"
        self.assertNotEqual(codigo(a), codigo(b))

    def test_limite_de_orcamento(self):
        d = normalizar(plano_base(orcamento_diario=120), "1234567890")
        erros, _ = validar(d, orcamento_maximo=66)
        self.assertTrue(any("limite configurado" in e for e in erros))

    def test_titulo_longo_e_exclamacao(self):
        p = plano_base()
        p.grupos[0].anuncios[0].titulos[0] = "Um título comprido demais para o Google Ads"
        p.grupos[0].anuncios[0].titulos[1] = "Teste agora!"
        erros, _ = validar(normalizar(p, "1234567890"))
        self.assertTrue(any("caracteres" in e for e in erros))
        self.assertTrue(any("'!'" in e for e in erros))

    def test_negativa_que_bloqueia_palavra_chave(self):
        p = plano_base(negativas=[{"texto": "varios atendentes"}])
        erros, _ = validar(normalizar(p, "1234567890"))
        self.assertTrue(any("bloqueia" in e for e in erros))

    def test_conta_ausente(self):
        erros, _ = validar(normalizar(plano_base(), None))
        self.assertTrue(any("Conta" in e for e in erros))

    def test_grupo_sem_anuncio(self):
        p = plano_base()
        p.grupos[0].anuncios = []
        erros, _ = validar(normalizar(p, "1234567890"))
        self.assertTrue(any("sem anúncio" in e for e in erros))


class TestOperacoes(unittest.TestCase):
    def setUp(self):
        self.cli = GoogleAdsClient(credentials=AnonymousCredentials(), developer_token="", use_proto_plus=True)

    def test_campanha_sempre_pausada_e_contagem(self):
        d = normalizar(plano_base(), "1234567890")
        ops, rotulos = operacoes.montar(self.cli, d)
        # orçamento, campanha, local, idioma, 2 negativas, grupo, 2 palavras-chave, 1 anúncio
        self.assertEqual(len(ops), 10)
        self.assertEqual(len(rotulos), 10)
        camp = ops[1].campaign_operation.create
        self.assertEqual(camp.status, self.cli.enums.CampaignStatusEnum.PAUSED)
        self.assertEqual(camp.target_spend.cpc_bid_ceiling_micros, 4_500_000)
        self.assertEqual(ops[0].campaign_budget_operation.create.amount_micros, 50_000_000)
        self.assertTrue(ops[4].campaign_criterion_operation.create.negative)

    def test_maximizar_conversoes(self):
        d = normalizar(plano_base(lance={"estrategia": "maximizar_conversoes", "cpa_alvo": 200}), "1234567890")
        ops, _ = operacoes.montar(self.cli, d)
        camp = ops[1].campaign_operation.create
        self.assertEqual(camp.maximize_conversions.target_cpa_micros, 200_000_000)
        self.assertEqual(type(camp).pb(camp).WhichOneof("campaign_bidding_strategy"), "maximize_conversions")

    def test_micros_arredonda_centavos(self):
        self.assertEqual(operacoes._micros(65.789), 65_790_000)


if __name__ == "__main__":
    unittest.main()
