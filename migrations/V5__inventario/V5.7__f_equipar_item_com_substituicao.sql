-- Função aprimorada para equipar itens com substituição automática
CREATE OR REPLACE FUNCTION f_equipar_item_com_substituicao(p_id_instancia_item INTEGER)
RETURNS TEXT AS $$
DECLARE
    v_id_personagem INTEGER;
    v_id_item INTEGER;
    v_tipo_equipavel VARCHAR(50);
    v_tipo_armadura VARCHAR(50);
    v_nome_item VARCHAR(50);
    v_item_anterior INTEGER;
    v_capacidade INTEGER;
    v_itens_atual INTEGER;
    v_resultado TEXT;
BEGIN
    -- Obter informações do item e personagem
    SELECT inv.id_personagem, ii.id_item, i.nome
    INTO v_id_personagem, v_id_item, v_nome_item
    FROM INVENTARIO_ITENS inv
    JOIN INSTANCIA_ITEM ii ON inv.id_instancia = ii.id_instancia
    JOIN ITEM i ON ii.id_item = i.id_item
    WHERE inv.id_instancia = p_id_instancia_item;

    IF v_id_personagem IS NULL THEN
        RETURN 'ERRO: Item não encontrado no inventário.';
    END IF;

    -- Verificar se é equipável
    SELECT e.tipo_equipavel
    INTO v_tipo_equipavel
    FROM EQUIPAVEL e
    WHERE e.id_item = v_id_item;

    IF v_tipo_equipavel IS NULL THEN
        RETURN 'ERRO: Item não é equipável.';
    END IF;

    -- Verificar capacidade do inventário
    SELECT i.capacidade, COUNT(ii.id_instancia)
    INTO v_capacidade, v_itens_atual
    FROM INVENTARIO i
    LEFT JOIN INVENTARIO_ITENS ii ON i.id_personagem = ii.id_personagem
    WHERE i.id_personagem = v_id_personagem
    GROUP BY i.capacidade;

    -- Verificar item anterior no slot e mover para inventário se necessário
    IF v_tipo_equipavel = 'Arma' THEN
        -- Verificar slot de arma
        SELECT slot_arma INTO v_item_anterior
        FROM INVENTARIO_EQUIPADOS
        WHERE id_personagem = v_id_personagem AND slot_arma IS NOT NULL;
        
        IF v_item_anterior IS NOT NULL THEN
            -- Verificar espaço no inventário
            IF v_itens_atual >= v_capacidade THEN
                RETURN 'ERRO: Inventário cheio! Não é possível substituir o item equipado.';
            END IF;
            
            -- Mover item anterior para inventário
            INSERT INTO INVENTARIO_ITENS (id_personagem, id_instancia)
            VALUES (v_id_personagem, v_item_anterior);
        END IF;
        
        -- Equipar novo item
        UPDATE INVENTARIO_EQUIPADOS
        SET slot_arma = p_id_instancia_item
        WHERE id_personagem = v_id_personagem;

    ELSIF v_tipo_equipavel = 'Armadura' THEN
        -- Determinar tipo de armadura
        SELECT CASE
            WHEN i.nome ILIKE '%Peitoral%' THEN 'Peitoral'
            WHEN i.nome ILIKE '%Capacete%' THEN 'Capacete'
            WHEN i.nome ILIKE '%Escudo%' THEN 'Escudo'
            ELSE NULL
        END INTO v_tipo_armadura
        FROM ITEM i WHERE i.id_item = v_id_item;

        IF v_tipo_armadura = 'Peitoral' THEN
            SELECT slot_armadura_peitoral INTO v_item_anterior
            FROM INVENTARIO_EQUIPADOS
            WHERE id_personagem = v_id_personagem AND slot_armadura_peitoral IS NOT NULL;
            
            IF v_item_anterior IS NOT NULL THEN
                IF v_itens_atual >= v_capacidade THEN
                    RETURN 'ERRO: Inventário cheio! Não é possível substituir o item equipado.';
                END IF;
                INSERT INTO INVENTARIO_ITENS (id_personagem, id_instancia)
                VALUES (v_id_personagem, v_item_anterior);
            END IF;
            
            UPDATE INVENTARIO_EQUIPADOS
            SET slot_armadura_peitoral = p_id_instancia_item
            WHERE id_personagem = v_id_personagem;

        ELSIF v_tipo_armadura = 'Capacete' THEN
            SELECT slot_armadura_capacete INTO v_item_anterior
            FROM INVENTARIO_EQUIPADOS
            WHERE id_personagem = v_id_personagem AND slot_armadura_capacete IS NOT NULL;
            
            IF v_item_anterior IS NOT NULL THEN
                IF v_itens_atual >= v_capacidade THEN
                    RETURN 'ERRO: Inventário cheio! Não é possível substituir o item equipado.';
                END IF;
                INSERT INTO INVENTARIO_ITENS (id_personagem, id_instancia)
                VALUES (v_id_personagem, v_item_anterior);
            END IF;
            
            UPDATE INVENTARIO_EQUIPADOS
            SET slot_armadura_capacete = p_id_instancia_item
            WHERE id_personagem = v_id_personagem;
        
        ELSIF v_tipo_armadura = 'Escudo' THEN
            SELECT slot_armadura_escudo INTO v_item_anterior
            FROM INVENTARIO_EQUIPADOS
            WHERE id_personagem = v_id_personagem AND slot_armadura_escudo IS NOT NULL;
            
            IF v_item_anterior IS NOT NULL THEN
                IF v_itens_atual >= v_capacidade THEN
                    RETURN 'ERRO: Inventário cheio! Não é possível substituir o item equipado.';
                END IF;
                INSERT INTO INVENTARIO_ITENS (id_personagem, id_instancia)
                VALUES (v_id_personagem, v_item_anterior);
            END IF;
            
            UPDATE INVENTARIO_EQUIPADOS
            SET slot_armadura_escudo = p_id_instancia_item
            WHERE id_personagem = v_id_personagem;

        ELSE
            RETURN 'ERRO: Tipo de armadura não reconhecido.';
        END IF;

    ELSIF v_tipo_equipavel = 'Artefato' THEN
        -- Verificar se é espiritualista
        IF NOT EXISTS (SELECT 1 FROM ESPIRITUALISTA WHERE id_personagem = v_id_personagem) THEN
            RETURN 'ERRO: Apenas espiritualistas podem equipar artefatos.';
        END IF;
        
        SELECT slot_artefato INTO v_item_anterior
        FROM ESPIRITUALISTA
        WHERE id_personagem = v_id_personagem AND slot_artefato IS NOT NULL;
        
        IF v_item_anterior IS NOT NULL THEN
            IF v_itens_atual >= v_capacidade THEN
                RETURN 'ERRO: Inventário cheio! Não é possível substituir o item equipado.';
            END IF;
            INSERT INTO INVENTARIO_ITENS (id_personagem, id_instancia)
            VALUES (v_id_personagem, v_item_anterior);
        END IF;
        
        UPDATE ESPIRITUALISTA
        SET slot_artefato = p_id_instancia_item
        WHERE id_personagem = v_id_personagem;

    ELSE
        RETURN 'ERRO: Tipo de item não reconhecido.';
    END IF;

    -- Remover item do inventário normal
    DELETE FROM INVENTARIO_ITENS 
    WHERE id_personagem = v_id_personagem AND id_instancia = p_id_instancia_item;

    v_resultado := 'Item ' || v_nome_item || ' equipado com sucesso.';
    IF v_item_anterior IS NOT NULL THEN
        v_resultado := v_resultado || ' Item anterior movido para o inventário.';
    END IF;

    RETURN v_resultado;

EXCEPTION
    WHEN OTHERS THEN
        RETURN 'ERRO: ' || SQLERRM;
END;
$$ LANGUAGE plpgsql;