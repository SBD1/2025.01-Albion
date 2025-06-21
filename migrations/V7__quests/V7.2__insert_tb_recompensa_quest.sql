-- Insert rewards for quests
INSERT INTO
    RECOMPENSA_QUEST (
        id_quest,
        item_recompensa,
        quantidade,
        gold
    )
VALUES
    -- Quest do John Mercador (ID 1)
    (
        1,
        (
            SELECT id_item
            FROM ITEM
            WHERE
                nome = 'Pão de Centeio'
        ),
        5,
        5000
    ), -- 5 Pães de Centeio + 5000 gold

-- Quest da Aeliana (ID 2)
(
    2,
    (
        SELECT id_item
        FROM ITEM
        WHERE
            nome = 'Orbe do Destino'
    ),
    1,
    7500
), -- Orbe do Destino + 7500 gold

-- Quest do Faelar Bosquevir (ID 3)
(
    3,
    (
        SELECT id_item
        FROM ITEM
        WHERE
            nome = 'Peitoral de Mithril'
    ),
    1,
    3000
), -- Peitoral de Mithril + 3000 gold

-- Quest do Thrain Ferreiro (ID 4)
(
    4,
    (
        SELECT id_item
        FROM ITEM
        WHERE
            nome = 'Espada de Adamantium'
    ),
    1,
    4000
), -- Espada de Adamantium + 4000 gold

-- Quest do Vek'thor O Amaldiçoado (ID 5)
(
    5,
    (
        SELECT id_item
        FROM ITEM
        WHERE
            nome = 'Grimório Arcano'
    ),
    1,
    8000
);
-- Grimório Arcano + 8000 gold

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