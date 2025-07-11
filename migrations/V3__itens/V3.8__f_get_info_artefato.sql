CREATE OR REPLACE FUNCTION f_get_info_artefato(
    p_id_instancia INTEGER
)
RETURNS TABLE (
    nome_artefato VARCHAR,
    descricao TEXT,
    aumento_ataque_magico INTEGER,
    aumento_mana_maxima INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.nome AS nome_artefato,
        i.descricao,
        a.aumento_ataque_magico,
        a.aumento_mana_maxima
    FROM 
        INSTANCIA_ITEM ii
    JOIN 
        ITEM i ON ii.id_item = i.id_item
    JOIN 
        EQUIPAVEL e ON i.id_item = e.id_item
    JOIN 
        ARTEFATO a ON e.id_item = a.id_item
    WHERE 
        ii.id_instancia = p_id_instancia;
END;
$$ LANGUAGE plpgsql;