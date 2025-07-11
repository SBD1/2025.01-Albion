-- Tabela de Magias para Espiritualistas - RPG Albion
CREATE TABLE IF NOT EXISTS MAGIA (
    id_magia SERIAL PRIMARY KEY,
    nome VARCHAR(50) UNIQUE NOT NULL,
    descricao TEXT NOT NULL,
    nivel_requerido INTEGER NOT NULL DEFAULT 1,
    custo_mana INTEGER NOT NULL,
    dano_base INTEGER DEFAULT 0,
    cura_base INTEGER DEFAULT 0
);