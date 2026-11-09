"""Classe Usuario com as operações de CRUD.

CREATE -> salvar()
READ   -> listar() e buscar_por_id()
UPDATE -> atualizar()
DELETE -> excluir()

Todos os métodos que alteram dados devolvem (sucesso: bool, mensagem: str).
"""

from mysql.connector import errorcode, Error

from conector import Conector
from seguranca import gerar_hash


def _fechar(cursor, conexao):
    if cursor is not None:
        cursor.close()
    if conexao is not None and conexao.is_connected():
        conexao.close()


class Usuario:
    def __init__(self, nome, email, senha, id=None):
        self.id = id
        self.nome = nome.strip()
        self.email = email.strip().lower()
        self.senha = senha

    # ---------- CREATE ----------
    def salvar(self):
        conexao = Conector().conectar()
        if conexao is None:
            return False, "Não foi possível conectar ao banco."

        cursor = conexao.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)",
                (self.nome, self.email, gerar_hash(self.senha)),
            )
            conexao.commit()
            self.id = cursor.lastrowid
            return True, "Usuário cadastrado com sucesso!"

        except Error as erro:
            if erro.errno == errorcode.ER_DUP_ENTRY:
                return False, "Esse e-mail já está cadastrado."
            return False, f"Erro ao cadastrar usuário: {erro}"

        finally:
            _fechar(cursor, conexao)

    # ---------- READ ----------
    @staticmethod
    def listar():
        conexao = Conector().conectar()
        if conexao is None:
            return []

        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, nome, email FROM usuarios ORDER BY nome ASC")
            return cursor.fetchall()
        except Error as erro:
            print(f"Erro ao listar usuários: {erro}")
            return []
        finally:
            _fechar(cursor, conexao)

    @staticmethod
    def buscar_por_id(id):
        conexao = Conector().conectar()
        if conexao is None:
            return None

        cursor = conexao.cursor(dictionary=True)
        try:
            cursor.execute("SELECT id, nome, email FROM usuarios WHERE id = %s", (id,))
            return cursor.fetchone()
        except Error as erro:
            print(f"Erro ao buscar usuário: {erro}")
            return None
        finally:
            _fechar(cursor, conexao)

    # ---------- UPDATE ----------
    def atualizar(self, id):
        conexao = Conector().conectar()
        if conexao is None:
            return False, "Não foi possível conectar ao banco."

        cursor = conexao.cursor()
        try:
            if self.senha:
                cursor.execute(
                    "UPDATE usuarios SET nome = %s, email = %s, senha = %s WHERE id = %s",
                    (self.nome, self.email, gerar_hash(self.senha), id),
                )
            else:
                cursor.execute(
                    "UPDATE usuarios SET nome = %s, email = %s WHERE id = %s",
                    (self.nome, self.email, id),
                )
            conexao.commit()

            # rowcount pode ser 0 quando nada mudou; por isso confirmamos se o id existe
            if cursor.rowcount == 0:
                cursor.execute("SELECT 1 FROM usuarios WHERE id = %s", (id,))
                if cursor.fetchone() is None:
                    return False, "Usuário não encontrado."

            return True, "Usuário atualizado com sucesso!"

        except Error as erro:
            if erro.errno == errorcode.ER_DUP_ENTRY:
                return False, "Esse e-mail já está cadastrado."
            return False, f"Erro ao atualizar usuário: {erro}"

        finally:
            _fechar(cursor, conexao)

    # ---------- DELETE ----------
    @staticmethod
    def excluir(id):
        conexao = Conector().conectar()
        if conexao is None:
            return False, "Não foi possível conectar ao banco."

        cursor = conexao.cursor()
        try:
            cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
            conexao.commit()

            if cursor.rowcount == 0:
                return False, "Usuário não encontrado."
            return True, "Usuário excluído com sucesso!"

        except Error as erro:
            return False, f"Erro ao excluir usuário: {erro}"

        finally:
            _fechar(cursor, conexao)
