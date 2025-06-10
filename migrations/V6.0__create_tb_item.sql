-- Superclasse - Item --
CREATE TABLE IF NOT EXISTS ITEM (
    nome VARCHAR(100) PRIMARY KEY,
    descricao TEXT,
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
    dano INTEGER NOT NULL,
    ataque_fisico INTEGER NOT NULL,
    stamina_maxima INTEGER NOT NULL
);
--Subclasse Equipavel - Armadura --
CREATE TABLE IF NOT EXISTS ARMADURA (
    nome_armadura VARCHAR(100) PRIMARY KEY REFERENCES public.EQUIPAVEL (nome_equipavel),
    defesa_fisica INTEGER NOT NULL,
    defesa_magica INTEGER NOT NULL,
    vida_maxima INTEGER NOT NULL
);
--Subclasse Equipavel - Artefato --
CREATE TABLE IF NOT EXISTS ARTEFATO (
    nome_artefato VARCHAR(100) PRIMARY KEY REFERENCES public.EQUIPAVEL (nome_equipavel),
    dano INTEGER NOT NULL,
    ataque_magico INTEGER NOT NULL,
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
    stamina_atual INTEGER NOT NULL
);

--Subclasse N-equipavel - Pocao --
CREATE TABLE IF NOT EXISTS POCAO (
    nome_pocao VARCHAR(100) PRIMARY KEY REFERENCES public.NEQUIPAVEL (nome_nequipavel),
    mana_atual INTEGER NOT NULL
);

/* CREATE TABLE IF NOT EXISTS ITEM (
    nome VARCHAR(100) PRIMARY KEY,
    descriçao TEXT,
    tipo_item VARCHAR(50) NOT NULL CHECK (
        tipo_item IN ('Equipavel', 'Nao-Equipavel')
    )
)

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
    ),
    CONSTRAINT check_equipavel CHECK (
        (
            SELECT tipo_item
            FROM public.ITEM
            WHERE
                public.ITEM.nome = public.EQUIPAVEL.nome_equipavel
        ) = 'Equipavel'
    )
)
-- Subclasse Equipavel - Arma --
CREATE TABLE IF NOT EXISTS ARMA (
    nome_arma VARCHAR(100) PRIMARY KEY REFERENCES public.EQUIPAVEL (nome_equipavel),
    dano INTEGER NOT NULL,
    ataque_fisico INTEGER NOT NULL,
    stamina_maxima INTEGER NOT NULL,
    CONSTRAINT check_arma CHECK (
        (
            SELECT tipo_equipavel
            FROM public.EQUIPAVEL e
            WHERE
                public.EQUIPAVEL.nome_equipavel = ARMA.nome_arma
        ) = 'Arma'
    )
)
--Subclasse Equipavel - Armadura --
CREATE TABLE IF NOT EXISTS ARMADURA (
    nome_armadura VARCHAR(100) PRIMARY KEY REFERENCES public.EQUIPAVEL (nome_equipavel),
    defesa_fisica INTEGER NOT NULL,
    defesa_magica INTEGER NOT NULL,
    vida_maxima INTEGER NOT NULL,
    CONSTRAINT check_armadura CHECK (
        (
            SELECT tipo_equipavel
            FROM public.EQUIPAVEL
            where
                public.EQUIPAVEL.nome_equipavel = public.ARMADURA.nome_armadura
        ) = 'Armadura'
    )
)
--Subclasse Equipavel - Artefato --
CREATE TABLE IF NOT EXISTS ARTEFATO (
    nome_artefato VARCHAR(100) PRIMARY KEY REFERENCES public.EQUIPAVEL (nome_equipavel),
    dano INTEGER NOT NULL,
    ataque_magico INTEGER NOT NULL,
    mana_maxima INTEGER NOT NULL,
    CONSTRAINT check_artefato CHECK (
        (
            SELECT tipo_equipavel
            FROM public.EQUIPAVEL
            WHERE
                public.EQUIPAVEL.nome_equipavel = public.ARTEFATO.nome_artefato
        ) = 'Artefato'
    )
)
-- Subclasse Item - Nao-equipavel --
CREATE TABLE IF NOT EXISTS NEQUIPAVEL (
    nome_nequipavel VARCHAR(100) PRIMARY KEY REFERENCES public.ITEM (nome),
    quantidade INTEGER NOT NULL,
    tipo_nequipavel VARCHAR(100) NOT NULL CHECK (
        tipo_nequipavel in ('Comida', 'Poçao')
    ),
    CONSTRAINT check_nequipavel CHECK (
        (
            SELECT tipo_item
            FROM public.ITEM
            WHERE
                public.ITEM.nome = public.NEQUIPAVEL.nome_nequipavel
        ) = 'Nao-Equipavel'
    )
)
-- Subclasse N-equipavel - Comida --
CREATE TABLE IF NOT EXISTS COMIDA (
    nome_comida VARCHAR(100) PRIMARY KEY REFERENCES public.NEQUIPAVEL (nome_nequipavel),
    stamina_atual INTEGER NOT NULL,
    CONSTRAINT check_comida CHECK (
        (
            SELECT tipo_nequipavel
            FROM public.NEQUIPAVEL
            WHERE
                public.NEQUIPAVEL.nome_nequipavel = public.COMIDA.nome_comida
        ) = 'Comida'
    )
)

--Subclasse N-equipavel - Poçao --
CREATE TABLE IF NOT EXISTS POÇAO (
    nome_poçao VARCHAR(100) PRIMARY KEY REFERENCES public.NEQUIPAVEL (nome_nequipavel),
    mana_atual INTEGER NOT NULL,
    CONSTRAINT check_poçao CHECK (
        (
            SELECT tipo_nequipavel
            FROM public.NEQUIPAVEL
            WHERE
                public.NEQUIPAVEL.nome_nequipavel = public.POÇAO.nome_poçao
        ) = 'Poçao'
    )
)"