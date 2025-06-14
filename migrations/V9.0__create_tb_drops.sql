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