-- Superclasse - Item --
CREATE TABLE IF NOT EXISTS ITEM (
    nome VARCHAR(100) PRIMARY KEY,
    descricao TEXT,
    nivel INTEGER NOT NULL,
    tipo_item VARCHAR(50) NOT NULL CHECK (
        tipo_item IN ('Equipavel', 'Nao-Equipavel')
    )
);
-- Subclasse Item - Equipáveis --
CREATE TABLE IF NOT EXISTS EQUIPAVEL (
    nome_equipavel VARCHAR(100) PRIMARY KEY REFERENCES public.ITEM (nome),
    durabilidade INTEGER NOT NULL,
    tipo_equipavel VARCHAR(50) NOT NULL CHECK (
        tipo_equipavel IN (
            'Arma',
            'Armadura',
            'Artefato'
        )
    )
);
-- Subclasse Equipavel - Arma --
CREATE TABLE IF NOT EXISTS ARMA (
    nome_arma VARCHAR(100) PRIMARY KEY REFERENCES public.EQUIPAVEL (nome_equipavel),
    aumento_ataque_fisico INTEGER NOT NULL
);
--Subclasse Equipavel - Armadura --
CREATE TABLE IF NOT EXISTS ARMADURA (
    nome_armadura VARCHAR(100) PRIMARY KEY REFERENCES public.EQUIPAVEL (nome_equipavel),
    aumento_defesa_fisica INTEGER,
    aumento_defesa_magica INTEGER,
    aumento_vida_maxima INTEGER NOT NULL
);
--Subclasse Equipavel - Artefato --
CREATE TABLE IF NOT EXISTS ARTEFATO (
    nome_artefato VARCHAR(100) PRIMARY KEY REFERENCES public.EQUIPAVEL (nome_equipavel),
    aumento_ataque_magico INTEGER NOT NULL,
    mana_maxima INTEGER NOT NULL
);
-- Subclasse Item - Nao-equipavel --
CREATE TABLE IF NOT EXISTS NEQUIPAVEL (
    nome_nequipavel VARCHAR(100) PRIMARY KEY REFERENCES public.ITEM (nome),
    quantidade INTEGER NOT NULL,
    tipo_nequipavel VARCHAR(100) NOT NULL CHECK (
        tipo_nequipavel in ('Comida', 'Pocao')
    )
);
-- Subclasse N-equipavel - Comida --
CREATE TABLE IF NOT EXISTS COMIDA (
    nome_comida VARCHAR(100) PRIMARY KEY REFERENCES public.NEQUIPAVEL (nome_nequipavel),
    aumento_vida_atual INTEGER NOT NULL,
    aumento_stamina_atual INTEGER NOT NULL
);
--Subclasse N-equipavel - Pocao --
CREATE TABLE IF NOT EXISTS POCAO (
    nome_pocao VARCHAR(100) PRIMARY KEY REFERENCES public.NEQUIPAVEL (nome_nequipavel),
    aumento_mana_atual INTEGER NOT NULL
);