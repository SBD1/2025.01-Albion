CREATE OR REPLACE FUNCTION f_get_tipo_item(
    p_id_instancia_item INTEGER
)
RETURNS VARCHAR AS $$
DECLARE
    v_tipo_item VARCHAR;
BEGIN
    SELECT i.tipo_item
    INTO v_tipo_item
    FROM INSTANCIA_ITEM ii
    JOIN ITEM i
    ON ii.id_item = i.id_item
    WHERE ii.id_instancia = p_id_instancia_item;

    IF v_tipo_item IS NULL THEN
        RAISE EXCEPTION 'Item com id_item % não encontrado.', p_id_item;
    END IF;

    RETURN v_tipo_item;
END;
$$ LANGUAGE plpgsql;