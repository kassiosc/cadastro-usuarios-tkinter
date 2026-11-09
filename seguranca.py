"""Hash e verificação de senhas usando apenas a biblioteca padrão do Python.

Formato guardado no banco:  pbkdf2_sha256$<iterações>$<salt em hex>$<hash em hex>

Cada senha ganha um salt aleatório, então duas pessoas com a mesma senha
terminam com hashes diferentes, o que o SHA-256 simples não garante.
"""

import hashlib
import hmac
import secrets

ALGORITMO = "pbkdf2_sha256"
ITERACOES = 600_000


def gerar_hash(senha: str) -> str:
    salt = secrets.token_hex(16)
    derivado = hashlib.pbkdf2_hmac(
        "sha256", senha.encode("utf-8"), bytes.fromhex(salt), ITERACOES
    )
    return f"{ALGORITMO}${ITERACOES}${salt}${derivado.hex()}"


def verificar_senha(senha: str, hash_guardado: str) -> bool:
    try:
        algoritmo, iteracoes, salt, esperado = hash_guardado.split("$")
        if algoritmo != ALGORITMO:
            return False
        derivado = hashlib.pbkdf2_hmac(
            "sha256", senha.encode("utf-8"), bytes.fromhex(salt), int(iteracoes)
        )
    except (ValueError, TypeError):
        return False

    # compare_digest evita ataques de tempo na comparação
    return hmac.compare_digest(derivado.hex(), esperado)
