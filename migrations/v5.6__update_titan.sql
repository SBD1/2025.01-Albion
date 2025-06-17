-- Atualizar slot_extra_arma_1
CREATE OR REPLACE FUNCTION f_atualiza_slot_extra_arma_1_personagem(
    p_id_personagem INTEGER,
    p_novo_slot_extra_arma_1 INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET slot_extra_arma_1 = p_novo_slot_extra_arma_1
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;

-- Atualizar slot_extra_arma_2
CREATE OR REPLACE FUNCTION f_atualiza_slot_extra_arma_2_personagem(
    p_id_personagem INTEGER,
    p_novo_slot_extra_arma_2 INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET slot_extra_arma_2 = p_novo_slot_extra_arma_2
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;