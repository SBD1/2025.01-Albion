-- Função para consumir um item e aplicar seus efeitos
CREATE OR REPLACE FUNCTION f_consumir_item(
    p_id_personagem INTEGER,
    p_id_instancia INTEGER
)
RETURNS TEXT AS $$
DECLARE
    v_tipo_item VARCHAR(50);
    v_tipo_consumivel VARCHAR(100);
    v_id_item INTEGER;
    v_nome_item VARCHAR(50);
    v_aumento_vida INTEGER := 0;
    v_aumento_stamina INTEGER := 0;
    v_aumento_mana INTEGER := 0;
    v_resultado TEXT;
BEGIN
    -- Verificar se o item existe no inventário do personagem
    SELECT ii.id_item, i.nome, i.tipo_item
    INTO v_id_item, v_nome_item, v_tipo_item
    FROM INVENTARIO_ITENS inv
    JOIN INSTANCIA_ITEM ii ON inv.id_instancia = ii.id_instancia
    JOIN ITEM i ON ii.id_item = i.id_item
    WHERE inv.id_personagem = p_id_personagem 
    AND inv.id_instancia = p_id_instancia;
    
    IF NOT FOUND THEN
        RETURN 'ERRO: Item não encontrado no inventário.';
    END IF;
    
    -- Verificar se é consumível
    IF v_tipo_item != 'Nao-Equipavel' THEN
        RETURN 'ERRO: Este item não é consumível.';
    END IF;
    
    -- Obter tipo específico do consumível
    SELECT tipo_nequipavel INTO v_tipo_consumivel
    FROM NEQUIPAVEL WHERE id_item = v_id_item;
    
    -- Aplicar efeitos baseado no tipo
    IF v_tipo_consumivel = 'Comida' THEN
        -- Obter efeitos da comida
        SELECT aumento_vida_atual, aumento_stamina_atual
        INTO v_aumento_vida, v_aumento_stamina
        FROM COMIDA WHERE id_item = v_id_item;
        
        -- Aplicar efeitos (sem ultrapassar máximos)
        UPDATE PERSONAGEM 
        SET vida_atual = LEAST(vida_atual + v_aumento_vida, vida_maxima),
            stamina_atual = LEAST(stamina_atual + v_aumento_stamina, stamina_maxima)
        WHERE id_personagem = p_id_personagem;
        
        v_resultado := 'Você consumiu ' || v_nome_item || '! +' || v_aumento_vida || ' vida, +' || v_aumento_stamina || ' stamina.';
        
    ELSIF v_tipo_consumivel = 'Pocao' THEN
        -- Verificar se é espiritualista
        IF NOT EXISTS (SELECT 1 FROM ESPIRITUALISTA WHERE id_personagem = p_id_personagem) THEN
            RETURN 'ERRO: Apenas Espiritualistas podem usar poções de mana.';
        END IF;
        
        -- Obter efeitos da poção
        SELECT aumento_mana_atual INTO v_aumento_mana
        FROM POCAO WHERE id_item = v_id_item;
        
        -- Aplicar efeito (sem ultrapassar máximo)
        UPDATE ESPIRITUALISTA 
        SET mana_atual = LEAST(mana_atual + v_aumento_mana, mana_total)
        WHERE id_personagem = p_id_personagem;
        
        v_resultado := 'Você consumiu ' || v_nome_item || '! +' || v_aumento_mana || ' mana.';
    ELSE
        RETURN 'ERRO: Tipo de consumível não reconhecido.';
    END IF;
    
    -- Remover item do inventário
    DELETE FROM INVENTARIO_ITENS 
    WHERE id_personagem = p_id_personagem AND id_instancia = p_id_instancia;
    
    -- Remover instância do item
    DELETE FROM INSTANCIA_ITEM WHERE id_instancia = p_id_instancia;
    
    RETURN v_resultado;
    
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'ERRO: ' || SQLERRM;
END;
$$ LANGUAGE plpgsql;