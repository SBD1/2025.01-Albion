-- Função para equipar arma em slot específico para Titans
CREATE OR REPLACE FUNCTION f_equipar_arma_titan(
    p_id_personagem INTEGER,
    p_id_instancia INTEGER,
    p_slot_tipo VARCHAR(20) -- 'slot_arma', 'slot_extra_arma_1', 'slot_extra_arma_2'
)
RETURNS TEXT AS $$
DECLARE
    v_tipo_equipavel VARCHAR(50);
    v_nome_item VARCHAR(50);
BEGIN
    -- Verificar se o personagem é um Titan
    IF NOT EXISTS (SELECT 1 FROM TITAN WHERE id_personagem = p_id_personagem) THEN
        RETURN 'ERRO: Apenas Titans podem usar slots extras de arma.';
    END IF;
    
    -- Verificar se o item é uma arma
    SELECT e.tipo_equipavel, i.nome
    INTO v_tipo_equipavel, v_nome_item
    FROM INSTANCIA_ITEM ii
    JOIN ITEM i ON ii.id_item = i.id_item
    JOIN EQUIPAVEL e ON i.id_item = e.id_item
    WHERE ii.id_instancia = p_id_instancia;
    
    IF NOT FOUND THEN
        RETURN 'ERRO: Item não encontrado ou não é equipável.';
    END IF;
    
    IF v_tipo_equipavel != 'Arma' THEN
        RETURN 'ERRO: Este item não é uma arma.';
    END IF;
    
    -- Verificar se o item está no inventário do personagem
    IF NOT EXISTS (
        SELECT 1 FROM INVENTARIO_ITENS 
        WHERE id_personagem = p_id_personagem AND id_instancia = p_id_instancia
    ) THEN
        RETURN 'ERRO: Item não encontrado no inventário.';
    END IF;
    
    -- Equipar no slot específico
    IF p_slot_tipo = 'slot_arma' THEN
        -- Slot principal na tabela INVENTARIO_EQUIPADOS
        INSERT INTO INVENTARIO_EQUIPADOS (id_personagem, slot_arma) 
        VALUES (p_id_personagem, p_id_instancia)
        ON CONFLICT (id_personagem) 
        DO UPDATE SET slot_arma = p_id_instancia;
        
    ELSIF p_slot_tipo = 'slot_extra_arma_1' THEN
        -- Slot extra 1 na tabela TITAN
        UPDATE TITAN 
        SET slot_extra_arma_1 = p_id_instancia 
        WHERE id_personagem = p_id_personagem;
        
    ELSIF p_slot_tipo = 'slot_extra_arma_2' THEN
        -- Slot extra 2 na tabela TITAN
        UPDATE TITAN 
        SET slot_extra_arma_2 = p_id_instancia 
        WHERE id_personagem = p_id_personagem;
        
    ELSE
        RETURN 'ERRO: Tipo de slot inválido.';
    END IF;
    
    -- Remover do inventário (mover para equipado)
    DELETE FROM INVENTARIO_ITENS 
    WHERE id_personagem = p_id_personagem AND id_instancia = p_id_instancia;
    
    RETURN 'Arma ' || v_nome_item || ' equipada com sucesso no ' || p_slot_tipo || '.';
    
EXCEPTION
    WHEN OTHERS THEN
        RETURN 'ERRO: ' || SQLERRM;
END;
$$ LANGUAGE plpgsql;

-- Função para calcular ataque total considerando múltiplas armas para Titans
CREATE OR REPLACE FUNCTION f_calcular_ataque_total_titan(p_id_personagem INTEGER)
RETURNS INTEGER AS $$
DECLARE
    v_ataque_base INTEGER;
    v_ataque_total INTEGER := 0;
    v_ataque_arma INTEGER;
BEGIN
    -- Obter ataque base do personagem
    SELECT ataque_fisico INTO v_ataque_base
    FROM PERSONAGEM WHERE id_personagem = p_id_personagem;
    
    v_ataque_total := v_ataque_base;
    
    -- Somar ataque da arma principal (se equipada)
    SELECT COALESCE(a.aumento_ataque_fisico, 0) INTO v_ataque_arma
    FROM INVENTARIO_EQUIPADOS ie
    JOIN INSTANCIA_ITEM ii ON ie.slot_arma = ii.id_instancia
    JOIN ITEM i ON ii.id_item = i.id_item
    JOIN EQUIPAVEL e ON i.id_item = e.id_item
    JOIN ARMA a ON e.id_item = a.id_item
    WHERE ie.id_personagem = p_id_personagem;
    
    v_ataque_total := v_ataque_total + COALESCE(v_ataque_arma, 0);
    
    -- Se for Titan, somar ataques das armas extras
    IF EXISTS (SELECT 1 FROM TITAN WHERE id_personagem = p_id_personagem) THEN
        -- Arma extra 1
        SELECT COALESCE(a.aumento_ataque_fisico, 0) INTO v_ataque_arma
        FROM TITAN t
        JOIN INSTANCIA_ITEM ii ON t.slot_extra_arma_1 = ii.id_instancia
        JOIN ITEM i ON ii.id_item = i.id_item
        JOIN EQUIPAVEL e ON i.id_item = e.id_item
        JOIN ARMA a ON e.id_item = a.id_item
        WHERE t.id_personagem = p_id_personagem;
        
        v_ataque_total := v_ataque_total + COALESCE(v_ataque_arma, 0);
        
        -- Arma extra 2
        SELECT COALESCE(a.aumento_ataque_fisico, 0) INTO v_ataque_arma
        FROM TITAN t
        JOIN INSTANCIA_ITEM ii ON t.slot_extra_arma_2 = ii.id_instancia
        JOIN ITEM i ON ii.id_item = i.id_item
        JOIN EQUIPAVEL e ON i.id_item = e.id_item
        JOIN ARMA a ON e.id_item = a.id_item
        WHERE t.id_personagem = p_id_personagem;
        
        v_ataque_total := v_ataque_total + COALESCE(v_ataque_arma, 0);
    END IF;
    
    RETURN v_ataque_total;
END;
$$ LANGUAGE plpgsql;