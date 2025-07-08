CREATE OR REPLACE FUNCTION f_add_exp(
    p_id_personagem INTEGER,
    p_quantidade_exp INTEGER
)
RETURNS VOID AS $$
DECLARE
    v_exp_atual INTEGER;
    v_exp_maxima INTEGER;
    v_nivel_atual INTEGER;
BEGIN
    IF p_quantidade_exp < 0 THEN
        RAISE EXCEPTION 'A quantidade de experiência deve ser maior ou igual a 0. Valor recebido: %', p_quantidade_exp;
    END IF;

    SELECT exp_atual, exp_maxima, nivel
    INTO v_exp_atual, v_exp_maxima, v_nivel_atual
    FROM public.PERSONAGEM
    WHERE id_personagem = p_id_personagem;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Personagem com id % não encontrado.', p_id_personagem;
    END IF;

    v_exp_atual := v_exp_atual + p_quantidade_exp;

    WHILE v_exp_atual >= v_exp_maxima LOOP
        v_nivel_atual := v_nivel_atual + 1;
        v_exp_atual := v_exp_atual - v_exp_maxima;

        v_exp_maxima := CEIL(v_exp_maxima * 1.2);

        UPDATE public.PERSONAGEM
        SET vida_maxima = vida_maxima + 10,
            stamina_maxima = stamina_maxima + 5,
            ataque_fisico = ataque_fisico + 2,
            defesa_fisica = defesa_fisica + 2,
            defesa_magica = defesa_magica + 2
        WHERE id_personagem = p_id_personagem;
    END LOOP;

    UPDATE public.PERSONAGEM
    SET exp_atual = v_exp_atual,
        exp_maxima = v_exp_maxima,
        nivel = v_nivel_atual
    WHERE id_personagem = p_id_personagem;

    RAISE NOTICE 'Adicionado % experiência ao personagem com id %. Novo nível: %, Experiência atual: %/%.',
        p_quantidade_exp, p_id_personagem, v_nivel_atual, v_exp_atual, v_exp_maxima;
END;
$$ LANGUAGE plpgsql;