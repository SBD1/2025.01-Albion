-- Atualizar mana_total em ESPIRITUALISTA
CREATE OR REPLACE FUNCTION f_atualiza_mana_total_espiritualista(
    p_id_espiritualista INTEGER,
    p_nova_mana_total INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.espiritualista
    SET mana_total = p_nova_mana_total
    WHERE id_espiritualista = p_id_espiritualista;
END;
$$ LANGUAGE plpgsql;

-- Atualizar mana_atual em ESPIRITUALISTA
CREATE OR REPLACE FUNCTION f_atualiza_mana_atual_espiritualista(
    p_id_espiritualista INTEGER,
    p_nova_mana_atual INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.espiritualista
    SET mana_atual = p_nova_mana_atual
    WHERE id_espiritualista = p_id_espiritualista;
END;
$$ LANGUAGE plpgsql;

-- Atualizar slot_arma em PERSONAGEM
CREATE OR REPLACE FUNCTION f_atualiza_slot_arma_personagem(
    p_id_personagem INTEGER,
    p_novo_slot_arma INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET slot_arma = p_novo_slot_arma
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;

-- Atualizar slot_armadura em PERSONAGEM
CREATE OR REPLACE FUNCTION f_atualiza_slot_armadura_personagem(
    p_id_personagem INTEGER,
    p_novo_slot_armadura INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET slot_armadura = p_novo_slot_armadura
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;

-- Atualizar slot_artefato em PERSONAGEM
CREATE OR REPLACE FUNCTION f_atualiza_slot_artefato_personagem(
    p_id_personagem INTEGER,
    p_novo_slot_artefato INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET slot_artefato = p_novo_slot_artefato
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;