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

CREATE TABLE IF NOT EXISTS ZOIUDO (
    id_zoiudo SERIAL PRIMARY KEY,
    id_personagem INTEGER NOT NULL REFERENCES public.PERSONAGEM (id_personagem) ON DELETE CASCADE,
    controla_fantasma BOOLEAN NOT NULL DEFAULT TRUE,
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