-- Função para obter informações de comida
CREATE OR REPLACE FUNCTION f_get_info_comida(
    p_id_instancia INTEGER
)
RETURNS TABLE (
    nome VARCHAR,
    descricao TEXT,
    aumento_vida_atual INTEGER,
    aumento_stamina_atual INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.nome,
        i.descricao,
        c.aumento_vida_atual,
        c.aumento_stamina_atual
    FROM 
        INSTANCIA_ITEM ii
    JOIN 
        ITEM i ON ii.id_item = i.id_item
    JOIN 
        NEQUIPAVEL ne ON i.id_item = ne.id_item
    JOIN 
        COMIDA c ON ne.id_item = c.id_item
    WHERE 
        ii.id_instancia = p_id_instancia;
END;
$$ LANGUAGE plpgsql;