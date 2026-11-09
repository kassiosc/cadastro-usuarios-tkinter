-- Opcional: o próprio app cria o banco e a tabela na primeira execução.
-- Use este script se preferir criar tudo manualmente no MySQL.

CREATE DATABASE IF NOT EXISTS cadastro_usuario
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE cadastro_usuario;

CREATE TABLE IF NOT EXISTS usuarios (
    id    INT AUTO_INCREMENT PRIMARY KEY,
    nome  VARCHAR(100) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    senha VARCHAR(255) NOT NULL   -- hash PBKDF2 com salt, nunca a senha em texto
);

-- Usuário dedicado para o app (troque a senha!):
-- CREATE USER 'seu_usuario'@'localhost' IDENTIFIED BY 'sua_senha';
-- GRANT ALL PRIVILEGES ON cadastro_usuario.* TO 'seu_usuario'@'localhost';
