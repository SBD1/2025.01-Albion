-- Correção da função f_equipar_item para usar slot de artefato correto

CREATE OR REPLACE FUNCTION f_equipar_item(
    p_id_instancia_item INTEGER
)
RETURNS VOID AS $$
DECLARE
    v_id_personagem INTEGER;
    v_id_item INTEGER;
    v_tipo_equipavel VARCHAR(50);
    v_tipo_armadura VARCHAR(50);
BEGIN
    SELECT inv.id_personagem, ii.id_item
    INTO v_id_personagem, v_id_item
    FROM INVENTARIO_ITENS inv
    JOIN INSTANCIA_ITEM ii ON inv.id_instancia = ii.id_instancia
    WHERE inv.id_instancia = p_id_instancia_item;

    IF v_id_personagem IS NULL THEN
        RAISE EXCEPTION 'Item com id_instancia % não encontrado no inventário.', p_id_instancia_item;
    END IF;

    SELECT e.tipo_equipavel
    INTO v_tipo_equipavel
    FROM EQUIPAVEL e
    WHERE e.id_item = v_id_item;

    IF v_tipo_equipavel IS NULL THEN
        RAISE EXCEPTION 'Item com id_instancia % não é equipável.', p_id_instancia_item;
    END IF;

    IF v_tipo_equipavel = 'Arma' THEN
        UPDATE INVENTARIO_EQUIPADOS
        SET slot_arma = p_id_instancia_item
        WHERE id_personagem = v_id_personagem;

    ELSIF v_tipo_equipavel = 'Armadura' THEN
        SELECT CASE
            WHEN a.id_item IS NOT NULL AND i.nome ILIKE '%Peitoral%' THEN 'Peitoral'
            WHEN a.id_item IS NOT NULL AND i.nome ILIKE '%Capacete%' THEN 'Capacete'
            WHEN a.id_item IS NOT NULL AND i.nome ILIKE '%Escudo%' THEN 'Escudo'
            ELSE NULL
        END
        INTO v_tipo_armadura
        FROM ARMADURA a
        JOIN ITEM i ON a.id_item = i.id_item
        WHERE a.id_item = v_id_item;

        IF v_tipo_armadura = 'Peitoral' THEN
            UPDATE INVENTARIO_EQUIPADOS
            SET slot_armadura_peitoral = p_id_instancia_item
            WHERE id_personagem = v_id_personagem;

        ELSIF v_tipo_armadura = 'Capacete' THEN
            UPDATE INVENTARIO_EQUIPADOS
            SET slot_armadura_capacete = p_id_instancia_item
            WHERE id_personagem = v_id_personagem;
        
        ELSIF v_tipo_armadura = 'Escudo' THEN
            UPDATE INVENTARIO_EQUIPADOS
            SET slot_armadura_escudo = p_id_instancia_item
            WHERE id_personagem = v_id_personagem;

        ELSE
            RAISE EXCEPTION 'Tipo de armadura não reconhecido para o item com id_instancia %.', p_id_instancia_item;
        END IF;

    ELSIF v_tipo_equipavel = 'Artefato' THEN
        IF NOT EXISTS (SELECT 1 FROM ESPIRITUALISTA WHERE id_personagem = v_id_personagem) THEN
            RAISE EXCEPTION 'Apenas espiritualistas podem equipar artefatos.';
        END IF;
        
        UPDATE ESPIRITUALISTA
        SET slot_artefato = p_id_instancia_item
        WHERE id_personagem = v_id_personagem;

    ELSE
        RAISE EXCEPTION 'Tipo de item não reconhecido: %', v_tipo_equipavel;
    END IF;

    RAISE NOTICE 'Item com id_instancia % equipado com sucesso.', p_id_instancia_item;
END;
$$ LANGUAGE plpgsql;