-- Insert rewards for quests
INSERT INTO RECOMPENSA_QUEST (id_quest, item_recompensa, quantidade, gold) VALUES
-- Orynth's Quest (Special NPC from Ancient Ruins)
(1, 101, 1, 5000),  -- Pergaminho Antigo + 5000 gold

-- Tho Mek's Quest (Special NPC from Nebulous Coast)
(2, 102, 1, 7500),  -- Cristal Luminoso + 7500 gold

-- Regular NPC Quests
(3, 103, 1, 1000),  -- Amuleto do Pescador + 1000 gold

(4, 104, 3, 2000),  -- Poção de Cura + 2000 gold

(5, 105, 1, 3000),  -- Minério Raro + 3000 gold

(6, 106, 1, 4000),  -- Chave Mágica + 4000 gold

(7, 107, 1, 3500),  -- Livro Proibido + 3500 gold

(8, 108, 2, 6000),  -- Poção Mágica + 6000 gold

(9, 109, 1, 4500),  -- Amuleto do Mercador + 4500 gold

(10, 110, 1, 10000); -- Cristal Elemental + 10000 gold

-- Trigger para entregar recompensas quando a quest for completada
CREATE OR REPLACE FUNCTION entregar_recompensa_quest()
RETURNS TRIGGER AS $$
BEGIN
    -- Só entrega recompensa se o status mudou para TRUE
    IF NEW.quest_status = TRUE AND (OLD.quest_status = FALSE OR OLD.quest_status IS NULL) THEN
        -- Adiciona o item ao inventário do personagem
        INSERT INTO INVENTARIO (id_personagem, id_item, quantidade)
        SELECT 
            NEW.id_personagem,
            rq.item_recompensa,
            rq.quantidade
        FROM RECOMPENSA_QUEST rq
        WHERE rq.id_quest = NEW.id_quest;

        -- Adiciona o gold ao personagem
        UPDATE PERSONAGEM
        SET gold = gold + (
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