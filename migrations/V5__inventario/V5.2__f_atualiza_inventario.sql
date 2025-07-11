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