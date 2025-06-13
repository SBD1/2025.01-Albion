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
    item_recompensa INTEGER NOT NULL REFERENCES public.ITEM (id_item),
    quantidade INTEGER NOT NULL DEFAULT 1,
    gold INTEGER NOT NULL DEFAULT 0
);