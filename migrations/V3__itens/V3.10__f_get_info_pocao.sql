CREATE OR REPLACE FUNCTION f_get_info_pocao(
    p_id_instancia INTEGER
)
RETURNS TABLE (
    nome VARCHAR,
    descricao TEXT,
    aumento_mana_atual INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.nome,
        i.descricao,
        p.aumento_mana_atual
    FROM 
        INSTANCIA_ITEM ii
    JOIN 
        ITEM i ON ii.id_item = i.id_item
    JOIN 
        NEQUIPAVEL ne ON i.id_item = ne.id_item
    JOIN 
        POCAO p ON ne.id_item = p.id_item
    WHERE 
        ii.id_instancia = p_id_instancia;
END;
$$ LANGUAGE plpgsql;