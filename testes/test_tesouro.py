import unittest
import vcr

from indicadores.tesouro import Tesouro


TesouroVcr = vcr.VCR(
    cassette_library_dir='testes/fixtures/',
)


class TesouroTestCase(unittest.TestCase):

    def setUp(self):
        self.tesouro = Tesouro('LTN', '2016')
        self.ltn_url = self.tesouro.URL_BASE + 'cosis/sistd/obtem_arquivo/319:39322'

    def test_inicializa_tesouro(self):
        self.assertIsInstance(self.tesouro, Tesouro)

    def test_extrai_tags_úteis(self):
        with TesouroVcr.use_cassette('histórico'):
            tags = self.tesouro._extrai_tags_úteis()
        self.assertEqual(len(tags), 113)

    def test_obtém_urls_tesouro(self):
        with TesouroVcr.use_cassette('histórico'):
            urls = self.tesouro._obtém_urls_tesouro()
        self.assertEqual(len(urls.keys()), 6)
        self.assertEqual(len(urls['LFT'].keys()), 17)
        self.assertEqual(urls['LTN']['2015'], self.ltn_url)
