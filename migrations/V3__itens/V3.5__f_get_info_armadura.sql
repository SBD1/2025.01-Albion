CREATE OR REPLACE FUNCTION f_get_info_armadura(
    p_id_instancia INTEGER
)
RETURNS TABLE (
    nome_armadura VARCHAR,
    descricao TEXT,
    aumento_defesa_fisica INTEGER,
    aumento_defesa_magica INTEGER,
    aumento_vida_maxima INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.nome AS nome_armadura,
        i.descricao,
        a.aumento_defesa_fisica,
        a.aumento_defesa_magica,
        a.aumento_vida_maxima
    FROM 
        INSTANCIA_ITEM ii
    JOIN 
        ITEM i ON ii.id_item = i.id_item
    JOIN 
        EQUIPAVEL e ON i.id_item = e.id_item
    JOIN 
        ARMADURA a ON e.id_item = a.id_item
    WHERE 
        ii.id_instancia = p_id_instancia;
END;
$$ LANGUAGE plpgsql;