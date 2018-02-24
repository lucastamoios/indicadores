from unittest import TestCase
from indicadores.tesouro import Tesouro


class TesouroTestCase(TestCase):

    def test_initialize_tesouro(self):
        self.assertIsInstance(Tesouro(), Tesouro)
