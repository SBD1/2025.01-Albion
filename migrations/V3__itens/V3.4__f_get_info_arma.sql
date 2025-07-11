CREATE OR REPLACE FUNCTION f_get_info_arma(
    p_id_instancia INTEGER
)
RETURNS TABLE (
    nome_arma VARCHAR,
    descricao TEXT,
    aumento_ataque_fisico INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.nome AS nome_arma,
        i.descricao,
        a.aumento_ataque_fisico
    FROM 
        INSTANCIA_ITEM ii
    JOIN 
        ITEM i ON ii.id_item = i.id_item
    JOIN 
        EQUIPAVEL e ON i.id_item = e.id_item
    JOIN 
        ARMA a ON e.id_item = a.id_item
    WHERE 
        ii.id_instancia = p_id_instancia;
END;
$$ LANGUAGE plpgsql;