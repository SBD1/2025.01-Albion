CREATE OR REPLACE FUNCTION atualizar_atributos_personagem()
RETURNS TRIGGER AS $$
DECLARE
    v_id_item INTEGER;
    v_ataque_fisico INTEGER := 0;
    v_def_fis INTEGER := 0;
    v_def_mag INTEGER := 0;
    v_vida_max INTEGER := 0;
    v_ataque_magico INTEGER := 0;
BEGIN
    -- ARMA
    IF NEW.slot_arma IS NOT NULL THEN
        SELECT id_item INTO v_id_item
        FROM INSTANCIA_ITEM WHERE id_instancia = NEW.slot_arma;

        SELECT COALESCE(a.aumento_ataque_fisico, 0)
        INTO v_ataque_fisico
        FROM ARMA a WHERE a.id_item = v_id_item;
    END IF;

    -- ARMADURA: PEITORAL
    IF NEW.slot_armadura_peitoral IS NOT NULL THEN
        SELECT id_item INTO v_id_item
        FROM INSTANCIA_ITEM WHERE id_instancia = NEW.slot_armadura_peitoral;

        SELECT 
            COALESCE(a.aumento_defesa_fisica, 0),
            COALESCE(a.aumento_defesa_magica, 0),
            COALESCE(a.aumento_vida_maxima, 0)
        INTO 
            v_def_fis, v_def_mag, v_vida_max
        FROM ARMADURA a WHERE a.id_item = v_id_item;
    END IF;

    -- ARMADURA: CAPACETE
    IF NEW.slot_armadura_capacete IS NOT NULL THEN
        SELECT id_item INTO v_id_item
        FROM INSTANCIA_ITEM WHERE id_instancia = NEW.slot_armadura_capacete;

        SELECT 
            COALESCE(a.aumento_defesa_fisica, 0),
            COALESCE(a.aumento_defesa_magica, 0),
            COALESCE(a.aumento_vida_maxima, 0)
        INTO 
            v_def_fis, v_def_mag, v_vida_max
        FROM ARMADURA a WHERE a.id_item = v_id_item;
    END IF;

    -- ARMADURA: ESCUDO
    IF NEW.slot_armadura_escudo IS NOT NULL THEN
        SELECT id_item INTO v_id_item
        FROM INSTANCIA_ITEM WHERE id_instancia = NEW.slot_armadura_escudo;

        SELECT 
            COALESCE(a.aumento_defesa_fisica, 0),
            COALESCE(a.aumento_defesa_magica, 0),
            COALESCE(a.aumento_vida_maxima, 0)
        INTO 
            v_def_fis, v_def_mag, v_vida_max
        FROM ARMADURA a WHERE a.id_item = v_id_item;
    END IF;

    -- ARTEFATO (para espiritualistas)
    IF EXISTS (
        SELECT 1 FROM ESPIRITUALISTA WHERE id_personagem = NEW.id_personagem
    ) THEN
        SELECT slot_artefato INTO v_id_item
        FROM ESPIRITUALISTA
        WHERE id_personagem = NEW.id_personagem;

        IF v_id_item IS NOT NULL THEN
            SELECT id_item INTO v_id_item
            FROM INSTANCIA_ITEM WHERE id_instancia = v_id_item;

            SELECT COALESCE(a.aumento_ataque_magico, 0)
            INTO v_ataque_magico
            FROM ARTEFATO a WHERE a.id_item = v_id_item;
        END IF;
    END IF;

    -- Atualiza os atributos do personagem
    UPDATE PERSONAGEM
    SET 
        ataque_fisico = 10 + v_ataque_fisico,
        defesa_fisica = 20 + v_def_fis,
        defesa_magica = 20 + v_def_mag,
        vida_maxima = 100 + v_vida_max
    WHERE id_personagem = NEW.id_personagem;

    -- Atualiza ataque mágico se for espiritualista
    IF EXISTS (
        SELECT 1 FROM ESPIRITUALISTA WHERE id_personagem = NEW.id_personagem
    ) THEN
        UPDATE ESPIRITUALISTA
        SET ataque_magico = 10 + v_ataque_magico
        WHERE id_personagem = NEW.id_personagem;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_atualiza_atributos_personagem
AFTER UPDATE ON INVENTARIO_EQUIPADOS
FOR EACH ROW
EXECUTE FUNCTION atualizar_atributos_personagem();
