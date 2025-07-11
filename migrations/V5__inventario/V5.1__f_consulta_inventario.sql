CREATE OR REPLACE FUNCTION f_consulta_inventario(p_id_personagem INTEGER)
RETURNS TABLE (
    id_instancia INTEGER,
    nome_item VARCHAR,
    descricao TEXT,
    quantidade INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ii.id_instancia,
        i.nome AS nome_item,
        i.descricao,
        ii.quantidade
    FROM 
        public.INVENTARIO_ITENS inv
    JOIN 
        public.INSTANCIA_ITEM ii ON inv.id_instancia = ii.id_instancia
    JOIN 
        public.ITEM i ON ii.id_item = i.id_item
    WHERE 
        inv.id_personagem = p_id_personagem
    ORDER BY 
        i.nome;
END;
$$ LANGUAGE plpgsql;