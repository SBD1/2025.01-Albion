
CREATE TABLE IF NOT EXISTS USUARIO(
    id_usuario   SERIAL PRIMARY KEY,
    username     VARCHAR(30) NOT NULL,
    password     VARCHAR(30) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(username)
);
