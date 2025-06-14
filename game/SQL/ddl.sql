CREATE TABLE IF NOT EXISTS USUARIO (
    id_usuario SERIAL PRIMARY KEY,
    username VARCHAR(30) NOT NULL,
    password VARCHAR(30) NOT NULL,
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (username)
);

CREATE TABLE IF NOT EXISTS SALA (
    id_sala SERIAL PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    descricao TEXT,
    conexao_norte INTEGER,
    conexao_sul INTEGER,
    conexao_leste INTEGER,
    conexao_oeste INTEGER
);

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

CREATE TABLE IF NOT EXISTS PERSONAGEM (
    id_personagem SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES public.USUARIO (id_usuario),
    id_sala INTEGER NOT NULL DEFAULT 1 REFERENCES public.SALA (id_sala) ON DELETE SET DEFAULT,
    nome VARCHAR(50) NOT NULL,
    nivel INTEGER NOT NULL DEFAULT 1,
    qtd_ouro INTEGER NOT NULL DEFAULT 0,
    exp_maxima INTEGER NOT NULL DEFAULT 100,
    exp_atual INTEGER NOT NULL DEFAULT 0,
    vida_atual INTEGER NOT NULL DEFAULT 100,
    vida_maxima INTEGER NOT NULL DEFAULT 100,
    stamina_atual INTEGER NOT NULL DEFAULT 100,
    stamina_maxima INTEGER NOT NULL DEFAULT 100,
    ataque_fisico INTEGER NOT NULL DEFAULT 10,
    defesa_fisica INTEGER NOT NULL DEFAULT 20,
    defesa_magica INTEGER NOT NULL DEFAULT 20,
    UNIQUE (nome)
);

CREATE TABLE IF NOT EXISTS FANTASMA (
    id_fantasma SERIAL PRIMARY KEY,
    nome VARCHAR(20),
    nivel INTEGER NOT NULL DEFAULT 1,
    exp_maxima INTEGER NOT NULL DEFAULT 100,
    exp_atual INTEGER NOT NULL DEFAULT 0,
    ataque_fisico INTEGER NOT NULL DEFAULT 1,
    ataque_magico INTEGER DEFAULT 10 NOT NULL,
    defesa_fisica INTEGER NOT NULL DEFAULT 10,
    defesa_magica INTEGER NOT NULL DEFAULT 10
);

CREATE TABLE IF NOT EXISTS ZOIUDO (
    id_zoiudo SERIAL PRIMARY KEY,
    id_personagem INTEGER NOT NULL REFERENCES public.PERSONAGEM (id_personagem) ON DELETE CASCADE,
    id_fantasma INTEGER UNIQUE REFERENCES public.FANTASMA (id_fantasma),
    UNIQUE (id_personagem)
);

CREATE TABLE IF NOT EXISTS ESPIRITUALISTA (
    id_espiritualista SERIAL PRIMARY KEY,
    id_personagem INTEGER NOT NULL REFERENCES public.PERSONAGEM (id_personagem) ON DELETE CASCADE,
    mana_total INTEGER DEFAULT 100 NOT NULL,
    mana_atual INTEGER DEFAULT 100 NOT NULL,
    ataque_magico INTEGER DEFAULT 10 NOT NULL,
    slot_artefato INTEGER UNIQUE REFERENCES public.INSTANCIA_ITEM (id_instancia),
    UNIQUE (id_personagem)
);

CREATE TABLE IF NOT EXISTS DRACONICO (
    id_draconico SERIAL PRIMARY KEY,
    id_personagem INTEGER NOT NULL REFERENCES public.PERSONAGEM (id_personagem) ON DELETE CASCADE,
    turnos_maximo_dragao INTEGER DEFAULT 3 NOT NULL,
    turnos_recarga INTEGER DEFAULT 5 NOT NULL,
    custo_stamina INTEGER DEFAULT 50 NOT NULL,
    aumento_vida_atual INTEGER DEFAULT 20 NOT NULL,
    aumento_ataque_fisico INTEGER DEFAULT 20 NOT NULL,
    UNIQUE (id_personagem)
);

CREATE TABLE IF NOT EXISTS TITAN (
    id_titan SERIAL PRIMARY KEY,
    id_personagem INTEGER NOT NULL REFERENCES public.PERSONAGEM (id_personagem) ON DELETE CASCADE,
    slot_extra_arma_1 INTEGER UNIQUE REFERENCES public.INSTANCIA_ITEM (id_instancia),
    slot_extra_arma_2 INTEGER UNIQUE REFERENCES public.INSTANCIA_ITEM (id_instancia),
    UNIQUE (id_personagem)
);

CREATE TABLE IF NOT EXISTS INVENTARIO (
    id_personagem INTEGER PRIMARY KEY REFERENCES public.PERSONAGEM (id_personagem),
    capacidade INTEGER NOT NULL DEFAULT 10
);

CREATE TABLE IF NOT EXISTS INVENTARIO_ITENS (
    id_personagem INTEGER NOT NULL REFERENCES public.INVENTARIO (id_personagem),
    id_instancia INTEGER UNIQUE NOT NULL REFERENCES public.INSTANCIA_ITEM (id_instancia),
    PRIMARY KEY (id_personagem, id_instancia)
);

CREATE TABLE IF NOT EXISTS INVENTARIO_EQUIPADOS (
    id_personagem INTEGER PRIMARY KEY REFERENCES public.PERSONAGEM (id_personagem),
    slot_arma INTEGER UNIQUE REFERENCES public.INSTANCIA_ITEM (id_instancia),
    slot_armadura_peitoral INTEGER UNIQUE REFERENCES public.INSTANCIA_ITEM (id_instancia),
    slot_armadura_capacete INTEGER UNIQUE REFERENCES public.INSTANCIA_ITEM (id_instancia),
    slot_armadura_escudo INTEGER UNIQUE REFERENCES public.INSTANCIA_ITEM (id_instancia)
);

CREATE TABLE IF NOT EXISTS NPC (
    id_npc SERIAL PRIMARY KEY,
    especie VARCHAR(50) NOT NULL,
    nome VARCHAR(50) UNIQUE,
    tipo VARCHAR(30) NOT NULL CHECK (tipo IN ('UNICO', 'GENERICO'))
);

CREATE TABLE IF NOT EXISTS NPC_UNICO (
    id_npc INTEGER PRIMARY KEY REFERENCES public.NPC (id_npc),
    posicao_x INTEGER NOT NULL,
    posicao_y INTEGER NOT NULL,
    UNIQUE (posicao_x, posicao_y),
    tipo VARCHAR(20) NOT NULL CHECK (tipo in ('BOSS', 'AMIGAVEL'))
);

CREATE TABLE IF NOT EXISTS NPC_BOSS (
    id_npc INTEGER PRIMARY KEY NOT NULL REFERENCES public.NPC_UNICO (id_npc),
    xp INTEGER NOT NULL,
    vida_maxima INTEGER NOT NULL DEFAULT 100,
    vida_atual INTEGER NOT NULL DEFAULT 100,
    ataque_fisico INTEGER NOT NULL DEFAULT 0,
    ataque_magico INTEGER NOT NULL DEFAULT 0,
    defesa_fisica INTEGER NOT NULL DEFAULT 0,
    defesa_magica INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS NPC_AMIGAVEL (
    id_npc INTEGER PRIMARY KEY NOT NULL REFERENCES public.NPC_UNICO (id_npc),
    faccao VARCHAR(50) CHECK (
        faccao in (
            'Culto das Sombras',
            'Igreja da Luz'
        )
    )
);

CREATE TABLE IF NOT EXISTS NPC_GENERICO (
    id_npc INTEGER PRIMARY KEY NOT NULL REFERENCES public.NPC (id_npc),
    xp INTEGER NOT NULL,
    vida_maxima INTEGER NOT NULL DEFAULT 100,
    ataque_fisico INTEGER NOT NULL DEFAULT 0,
    ataque_magico INTEGER NOT NULL DEFAULT 0,
    defesa_fisica INTEGER NOT NULL DEFAULT 0,
    defesa_magica INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS INSTANCIA_NPC_GENERICO (
    id_instancia SERIAL PRIMARY KEY,
    id_npc INTEGER NOT NULL REFERENCES public.NPC_GENERICO (id_npc),
    vida_atual INTEGER NOT NULL DEFAULT 100,
    posicao_x INTEGER NOT NULL,
    posicao_y INTEGER NOT NULL,
    UNIQUE (posicao_x, posicao_y)
);

CREATE TABLE IF NOT EXISTS QUEST (
    id_quest SERIAL PRIMARY KEY,
    id_npc INTEGER NOT NULL REFERENCES public.NPC_AMIGAVEL (id_npc),
    objetivo VARCHAR(250) NOT NULL,
    nivel_minimo INTEGER NOT NULL DEFAULT 1
);

CREATE TABLE IF NOT EXISTS INSTANCIA_QUEST (
    id_quest INTEGER NOT NULL REFERENCES public.QUEST (id_quest),
    id_personagem INTEGER NOT NULL REFERENCES public.PERSONAGEM (id_personagem),
    quest_status BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (id_quest, id_personagem)
);

CREATE TABLE IF NOT EXISTS RECOMPENSA_QUEST (
    id_recompensa SERIAL PRIMARY KEY,
    id_quest INTEGER NOT NULL REFERENCES public.QUEST (id_quest),
    item_recompensa INTEGER REFERENCES public.ITEM (id_item),
    quantidade INTEGER NOT NULL DEFAULT 0,
    gold INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS DROP_NPC (
    id_drop SERIAL PRIMARY KEY,
    id_npc INTEGER NOT NULL REFERENCES public.NPC (id_npc),
    tipo_npc VARCHAR(20) NOT NULL CHECK (
        tipo_npc IN ('BOSS', 'GENERICO')
    ),
    id_item INTEGER REFERENCES ITEM (id_item),
    quantidade_min INTEGER NOT NULL DEFAULT 1,
    quantidade_max INTEGER NOT NULL DEFAULT 1,
    probabilidade FLOAT NOT NULL CHECK (probabilidade BETWEEN 0 AND 1),
    gold_min INTEGER NOT NULL DEFAULT 0,
    gold_max INTEGER NOT NULL DEFAULT 0
);