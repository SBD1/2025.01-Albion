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