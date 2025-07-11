CREATE OR REPLACE FUNCTION f_get_tipo_item(
    p_id_instancia_item INTEGER
)
RETURNS VARCHAR AS $$
DECLARE
    v_tipo_equipavel VARCHAR;
    v_tipo_nequipavel VARCHAR;
    v_tipo_item VARCHAR;
BEGIN
    SELECT e.tipo_equipavel
    INTO v_tipo_equipavel
    FROM INSTANCIA_ITEM ii
    JOIN ITEM i ON ii.id_item = i.id_item
    JOIN EQUIPAVEL e ON i.id_item = e.id_item
    WHERE ii.id_instancia = p_id_instancia_item;

    IF v_tipo_equipavel IS NOT NULL THEN
        RETURN v_tipo_equipavel;
    END IF;

    SELECT ne.tipo_nequipavel
    INTO v_tipo_nequipavel
    FROM INSTANCIA_ITEM ii
    JOIN ITEM i ON ii.id_item = i.id_item
    JOIN NEQUIPAVEL ne ON i.id_item = ne.id_item
    WHERE ii.id_instancia = p_id_instancia_item;

    IF v_tipo_nequipavel IS NOT NULL THEN
        RETURN v_tipo_nequipavel;
    END IF;
    SELECT i.tipo_item
    INTO v_tipo_item
    FROM INSTANCIA_ITEM ii
    JOIN ITEM i ON ii.id_item = i.id_item
    WHERE ii.id_instancia = p_id_instancia_item;

    IF v_tipo_item IS NOT NULL THEN
        RETURN v_tipo_item;
    END IF;
    
    RAISE EXCEPTION 'Item com id_instancia % não encontrado.', p_id_instancia_item;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION f_get_info_item_basico(
    p_id_instancia INTEGER
)
RETURNS TABLE (
    nome VARCHAR,
    descricao TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.nome,
        i.descricao
    FROM 
        INSTANCIA_ITEM ii
    JOIN 
        ITEM i ON ii.id_item = i.id_item
    WHERE 
        ii.id_instancia = p_id_instancia;
END;
$$ LANGUAGE plpgsql;