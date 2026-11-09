"""Cria o banco de dados e a tabela de usuários (se ainda não existirem)."""

import mysql.connector
from mysql.connector import Error

import config


def criar_banco():
    conexao = None
    cursor = None

    try:
        conexao = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
        )
        cursor = conexao.cursor()

        cursor.execute(
            f"""
            CREATE DATABASE IF NOT EXISTS `{config.DB_NAME}`
            CHARACTER SET utf8mb4
            COLLATE utf8mb4_unicode_ci
            """
        )
        cursor.execute(f"USE `{config.DB_NAME}`")
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS usuarios (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(120) NOT NULL UNIQUE,
                senha VARCHAR(255) NOT NULL
            )
            """
        )
        conexao.commit()
        return True, f"Banco {config.DB_NAME} pronto."

    except Error as erro:
        return False, f"Não foi possível preparar o banco: {erro}"

    finally:
        if cursor is not None:
            cursor.close()
        if conexao is not None and conexao.is_connected():
            conexao.close()


if __name__ == "__main__":
    print(criar_banco()[1])
