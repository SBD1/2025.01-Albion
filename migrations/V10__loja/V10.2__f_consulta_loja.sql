CREATE OR REPLACE FUNCTION f_consulta_loja(
    p_nivel_personagem INTEGER DEFAULT NULL
)
RETURNS TABLE (
    id_item INTEGER,
    nome_item VARCHAR,
    preco INTEGER,
    quantidade_disponivel INTEGER,
    nivel_minimo INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        li.id_item,
        i.nome AS nome_item,
        li.preco,
        li.quantidade_disponivel,
        i.nivel AS nivel_minimo
    FROM 
        public.LOJA_ITENS li
    JOIN 
        public.ITEM i ON li.id_item = i.id_item
    WHERE i.nivel <= COALESCE(p_nivel_personagem, i.nivel)
    ORDER BY 
        li.preco;
END;
$$ LANGUAGE plpgsql;