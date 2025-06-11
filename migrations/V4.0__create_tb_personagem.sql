
CREATE TABLE IF NOT EXISTS PERSONAGEM(
    id_personagem  SERIAL PRIMARY KEY,
    id_usuario     INTEGER NOT NULL REFERENCES public.USUARIO(id_usuario),
    id_sala        INTEGER NOT NULL DEFAULT 1 REFERENCES public.SALA(id_sala) ON DELETE SET DEFAULT,
    nome           VARCHAR(50) NOT NULL,
    nivel          INTEGER NOT NULL DEFAULT 1, 
    qtd_ouro       INTEGER NOT NULL DEFAULT 0,
    experiencia    INTEGER NOT NULL DEFAULT 0,
    vida_atual     INTEGER NOT NULL DEFAULT 100,
    vida_maxima    INTEGER NOT NULL DEFAULT 100,
    stamina_atual  INTEGER NOT NULL DEFAULT 100,
    stamina_maxima INTEGER NOT NULL DEFAULT 100,
    ataque_fisico  INTEGER NOT NULL DEFAULT 10,
    ataque_magico  INTEGER NOT NULL DEFAULT 10,
    defesa_fisica  INTEGER NOT NULL DEFAULT 20,
    defesa_magica  INTEGER NOT NULL DEFAULT 20,
    UNIQUE(nome)
);

CREATE TABLE IF NOT EXISTS ZOIUDO(
    id_zoiudo         SERIAL PRIMARY KEY,
    id_personagem     INTEGER NOT NULL REFERENCES public.PERSONAGEM(id_personagem) ON DELETE CASCADE,
    controla_fantasma BOOLEAN NOT NULL DEFAULT TRUE,
    UNIQUE (id_personagem)
);

CREATE TABLE IF NOT EXISTS ESPIRITUALISTA(
    id_espiritualista SERIAL PRIMARY KEY,
    id_personagem     INTEGER NOT NULL REFERENCES public.PERSONAGEM(id_personagem) ON DELETE CASCADE,
    mana_total        INTEGER DEFAULT 100 NOT NULL,
    mana_atual        INTEGER DEFAULT 100 NOT NULL,
    UNIQUE (id_personagem)
);

CREATE TABLE IF NOT EXISTS DRACONICO(
    id_draconico    SERIAL PRIMARY KEY,
    id_personagem   INTEGER NOT NULL REFERENCES public.PERSONAGEM(id_personagem) ON DELETE CASCADE,
    tempo_em_dragao INTERVAL DEFAULT '00:01:00',
    UNIQUE (id_personagem)
);

CREATE TABLE IF NOT EXISTS TITAN(
    id_titan        SERIAL PRIMARY KEY,
    id_personagem   INTEGER NOT NULL REFERENCES public.PERSONAGEM(id_personagem) ON DELETE CASCADE,
    capacidade_item INTEGER NOT NULL DEFAULT 4,
    UNIQUE (id_personagem)
);