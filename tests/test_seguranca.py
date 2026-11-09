import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seguranca import gerar_hash, verificar_senha


class TestSeguranca(unittest.TestCase):
    def test_senha_correta_e_validada(self):
        h = gerar_hash("minha-senha")
        self.assertTrue(verificar_senha("minha-senha", h))

    def test_senha_errada_e_rejeitada(self):
        h = gerar_hash("minha-senha")
        self.assertFalse(verificar_senha("outra-senha", h))

    def test_mesma_senha_gera_hashes_diferentes(self):
        self.assertNotEqual(gerar_hash("abc12345"), gerar_hash("abc12345"))

    def test_hash_invalido_nao_quebra(self):
        self.assertFalse(verificar_senha("x", "isso-nao-e-um-hash"))
        self.assertFalse(verificar_senha("x", ""))


if __name__ == "__main__":
    unittest.main()
