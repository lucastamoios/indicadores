import unittest

from indicadores.tesouro import Tesouro


class TesouroTestCase(unittest.TestCase):

    def setUp(self):
        self.tesouro = Tesouro()
        self.ltn_url = self.tesouro.URL_BASE + 'cosis/sistd/obtem_arquivo/319:39322'

    def test_inicializa_tesouro(self):
        self.assertIsInstance(self.tesouro, Tesouro)
