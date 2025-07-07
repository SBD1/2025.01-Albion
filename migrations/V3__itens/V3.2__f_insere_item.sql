CREATE OR REPLACE FUNCTION f_insere_item(
    p_id_personagem INTEGER,
    p_id_item INTEGER,
    p_quantidade INTEGER
)
RETURNS VOID AS $$
DECLARE
    v_id_instancia INTEGER;
BEGIN
    INSERT INTO INSTANCIA_ITEM (id_item, quantidade)
    VALUES (p_id_item, p_quantidade)
    RETURNING id_instancia INTO v_id_instancia;

    INSERT INTO INVENTARIO_ITENS (id_personagem, id_instancia)
    VALUES (p_id_personagem, v_id_instancia);

    RAISE NOTICE 'Item inserido no inventário com sucesso!';
END;
$$ LANGUAGE plpgsql;