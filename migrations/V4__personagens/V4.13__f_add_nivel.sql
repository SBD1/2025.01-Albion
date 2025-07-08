CREATE OR REPLACE FUNCTION f_add_nivel(
    p_id_personagem INTEGER,
    p_qtd_nivel INTEGER
)
RETURNS VOID AS $$
BEGIN
    IF p_qtd_nivel < 0 THEN
        RAISE EXCEPTION 'A quantidade de ouro deve ser maior ou igual a 0. Valor recebido: %', p_qtd_nivel;
    END IF;

    UPDATE public.PERSONAGEM
    SET nivel = nivel + p_qtd_nivel
    WHERE id_personagem = p_id_personagem;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Personagem com id % não encontrado.', p_id_personagem;
    END IF;

    RAISE NOTICE 'Adicionado % níveis ao personagem com id %.', p_qtd_nivel, p_id_personagem;
END;
$$ LANGUAGE plpgsql;