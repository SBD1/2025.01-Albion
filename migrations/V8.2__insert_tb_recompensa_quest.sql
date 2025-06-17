-- Insert rewards for quests
INSERT INTO RECOMPENSA_QUEST (id_quest, item_recompensa, quantidade, gold) VALUES
-- Orynth's Quest (Special NPC from Ancient Ruins)
(1, (SELECT id_item FROM ITEM WHERE nome = 'Grimório Arcano'), 1, 5000),  -- Grimório Arcano + 5000 gold

-- Tho Mek's Quest (Special NPC from Nebulous Coast)
(2, (SELECT id_item FROM ITEM WHERE nome = 'Orbe do Destino'), 1, 7500),  -- Orbe do Destino + 7500 gold

-- Regular NPC Quests
(3, (SELECT id_item FROM ITEM WHERE nome = 'Colar da Serenidade'), 1, 1000),  -- Colar da Serenidade + 1000 gold

(4, (SELECT id_item FROM ITEM WHERE nome = 'Poção de Mana Forte'), 3, 2000),  -- 3 Poções de Mana Forte + 2000 gold

(5, (SELECT id_item FROM ITEM WHERE nome = 'Espada de Mithril'), 1, 3000),  -- Espada de Mithril + 3000 gold

(6, (SELECT id_item FROM ITEM WHERE nome = 'Coroa do Imperador'), 1, 4000),  -- Coroa do Imperador + 4000 gold

(7, (SELECT id_item FROM ITEM WHERE nome = 'Elixir Arcano'), 1, 3500),  -- Elixir Arcano + 3500 gold

(8, (SELECT id_item FROM ITEM WHERE nome = 'Poção de Mana Forte'), 2, 6000),  -- 2 Poções de Mana Forte + 6000 gold

(9, (SELECT id_item FROM ITEM WHERE nome = 'Peitoral de Mithril'), 1, 4500),  -- Peitoral de Mithril + 4500 gold

(10, (SELECT id_item FROM ITEM WHERE nome = 'Espada de Adamantium'), 1, 10000); -- Espada de Adamantium + 10000 gold

-- Trigger para entregar recompensas quando a quest for completada
CREATE OR REPLACE FUNCTION entregar_recompensa_quest()
RETURNS TRIGGER AS $$
DECLARE
    v_id_instancia INTEGER;
BEGIN
    -- Só entrega recompensa se o status mudou para TRUE
    IF NEW.quest_status = TRUE AND (OLD.quest_status = FALSE OR OLD.quest_status IS NULL) THEN
        -- Cria uma instância do item
        INSERT INTO INSTANCIA_ITEM (id_item, quantidade)
        SELECT 
            rq.item_recompensa,
            rq.quantidade
        FROM RECOMPENSA_QUEST rq
        WHERE rq.id_quest = NEW.id_quest
        RETURNING id_instancia INTO v_id_instancia;

        -- Adiciona o item ao inventário do personagem
        INSERT INTO INVENTARIO_ITENS (id_personagem, id_instancia)
        VALUES (NEW.id_personagem, v_id_instancia);

        -- Adiciona o gold ao personagem
        UPDATE PERSONAGEM
        SET qtd_ouro = qtd_ouro + (
            SELECT gold 
            FROM RECOMPENSA_QUEST 
            WHERE id_quest = NEW.id_quest
        )
        WHERE id_personagem = NEW.id_personagem;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Cria o trigger
CREATE TRIGGER trigger_entregar_recompensa
AFTER UPDATE ON INSTANCIA_QUEST
FOR EACH ROW
EXECUTE FUNCTION entregar_recompensa_quest(); 