CREATE OR REPLACE FUNCTION f_add_ouro(
    p_id_personagem INTEGER,
    p_quantidade_ouro INTEGER
)
RETURNS VOID AS $$
BEGIN
    IF p_quantidade_ouro < 0 THEN
        RAISE EXCEPTION 'A quantidade de ouro deve ser maior ou igual a 0. Valor recebido: %', p_quantidade_ouro;
    END IF;

    UPDATE public.PERSONAGEM
    SET qtd_ouro = qtd_ouro + p_quantidade_ouro
    WHERE id_personagem = p_id_personagem;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Personagem com id % não encontrado.', p_id_personagem;
    END IF;

    RAISE NOTICE 'Adicionado % ouro ao personagem com id %.', p_quantidade_ouro, p_id_personagem;
END;
$$ LANGUAGE plpgsql;