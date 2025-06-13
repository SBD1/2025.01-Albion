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