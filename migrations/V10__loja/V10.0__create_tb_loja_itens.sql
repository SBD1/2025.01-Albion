CREATE TABLE IF NOT EXISTS LOJA_ITENS (
    id_item INTEGER PRIMARY KEY REFERENCES public.ITEM (id_item) ON DELETE CASCADE,
    preco INTEGER NOT NULL CHECK (preco >= 0),
    quantidade_disponivel INTEGER NOT NULL DEFAULT 0 CHECK (quantidade_disponivel >= 0) 
);