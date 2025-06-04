CREATE TABLE IF NOT EXISTS USUARIO(
    id_usuario   SERIAL PRIMARY KEY,
    username     VARCHAR(30) NOT NULL,
    senha        VARCHAR(30) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS RACA(
    id_raca            SERIAL PRIMARY KEY,
    nome_raca          VARCHAR(50) NOT NULL,
    mult_defesa        DECIMAL(5,2) NOT NULL,
    mult_ataque_fisico DECIMAL(5,2) NOT NULL,
    mult_ataque_magico DECIMAL(5,2) NOT NULL    
);

CREATE TABLE IF NOT EXISTS PERSONAGEM(
    id_personagem   SERIAL PRIMARY KEY,
    id_raca         INTEGER REFERENCES RACA(idRaca) ON DELETE SET NULL,
    id_sala         INTEGER REFERENCES SALA(idSala) ON DELETE SET NULL,
    nome_personagem VARCHAR(50) NOT NULL,
    nivel           INTEGER NOT NULL,
    experiencia     INTEGER NOT NULL,
    stamina_atual   INTEGER NOT NULL,
    vida_atual      INTEGER NOT NULL,
    stamina_total   INTEGER NOT NULL,
    vida_total      INTEGER NOT NULL,
    defesa          INTEGER NOT NULL,
    ataque_fisico   INTEGER NOT NULL,
    ataque_magico   INTEGER NOT NULL
);

