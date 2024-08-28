-- Cria o banco de dados
CREATE DATABASE ka;

-- Conecta ao banco de dados criado
\c ka;

-- Cria a tabela 'empresas'
CREATE TABLE empresas (
    id_empresa SERIAL PRIMARY KEY,
    nome_empresa VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL
);

-- Cria a tabela 'funcionario'
CREATE TABLE funcionario (
    id_user SERIAL PRIMARY KEY,
    id_empresa INT REFERENCES empresas(id_empresa) ON DELETE CASCADE,
    nome VARCHAR(255) NOT NULL,
    senha VARCHAR(255) NOT NULL,
    cargo VARCHAR(100) NOT NULL,
    nome_empresa VARCHAR(255) NOT NULL
);

-- Cria a tabela 'pontos'
CREATE TABLE pontos (
    id_ponto SERIAL PRIMARY KEY,
    id_user INT REFERENCES funcionario(id_user) ON DELETE CASCADE,
    hora_inicio TIMESTAMP NOT NULL,
    hora_final TIMESTAMP
);
