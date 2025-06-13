-- Superclasse - Item --
CREATE TABLE IF NOT EXISTS ITEM (
    id_item SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    descricao TEXT,
    nivel INTEGER NOT NULL,
    tipo_item VARCHAR(50) NOT NULL CHECK (
        tipo_item IN ('Equipavel', 'Nao-Equipavel')
    )
);
-- Subclasse Item - Equipáveis --
CREATE TABLE IF NOT EXISTS EQUIPAVEL (
    id_item INTEGER PRIMARY KEY REFERENCES public.ITEM (id_item),
    durabilidade_maxima INTEGER NOT NULL,
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
    id_item INTEGER PRIMARY KEY REFERENCES public.EQUIPAVEL (id_item),
    aumento_ataque_fisico INTEGER NOT NULL
);
--Subclasse Equipavel - Armadura --
CREATE TABLE IF NOT EXISTS ARMADURA (
    id_item INTEGER PRIMARY KEY REFERENCES public.EQUIPAVEL (id_item),
    aumento_defesa_fisica INTEGER NOT NULL DEFAULT 0,
    aumento_defesa_magica INTEGER NOT NULL DEFAULT 0,
    aumento_vida_maxima INTEGER NOT NULL DEFAULT 0
);
--Subclasse Equipavel - Artefato --
CREATE TABLE IF NOT EXISTS ARTEFATO (
    id_item INTEGER PRIMARY KEY REFERENCES public.EQUIPAVEL (id_item),
    aumento_ataque_magico INTEGER NOT NULL,
    mana_maxima INTEGER NOT NULL
);
-- Subclasse Item - Nao-equipavel --
CREATE TABLE IF NOT EXISTS NEQUIPAVEL (
    id_item INTEGER PRIMARY KEY REFERENCES public.ITEM (id_item),
    tipo_nequipavel VARCHAR(100) NOT NULL CHECK (
        tipo_nequipavel in ('Comida', 'Pocao')
    )
);
-- Subclasse N-equipavel - Comida --
CREATE TABLE IF NOT EXISTS COMIDA (
    id_item INTEGER PRIMARY KEY REFERENCES public.NEQUIPAVEL (id_item),
    aumento_vida_atual INTEGER NOT NULL,
    aumento_stamina_atual INTEGER NOT NULL
);
--Subclasse N-equipavel - Pocao --
CREATE TABLE IF NOT EXISTS POCAO (
    id_item INTEGER PRIMARY KEY REFERENCES public.NEQUIPAVEL (id_item),
    aumento_mana_atual INTEGER NOT NULL
);

-- Tabela Instancia Item
CREATE TABLE IF NOT EXISTS INSTANCIA_ITEM (
    id_instancia SERIAL PRIMARY KEY,
    id_item INTEGER NOT NULL REFERENCES public.ITEM (id_item),
    durabilidade_atual INTEGER, -- NULL para não-equipáveis
    quantidade INTEGER NOT NULL DEFAULT 1 CHECK (quantidade >= 1)
);