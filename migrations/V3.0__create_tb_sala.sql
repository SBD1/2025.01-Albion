
CREATE TABLE IF NOT EXISTS SALA(
    id_sala       SERIAL PRIMARY KEY,
    nome          VARCHAR(50) NOT NULL,
    descricao     TEXT,
    conexao_norte INTEGER,
    conexao_sul   INTEGER,
    conexao_leste INTEGER,
    conexao_oeste INTEGER
);