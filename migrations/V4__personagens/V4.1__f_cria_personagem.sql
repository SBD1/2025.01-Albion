CREATE OR REPLACE FUNCTION f_cria_personagem(
    p_id_usuario      INTEGER,
    p_nome_personagem VARCHAR,
    p_especie_personagem VARCHAR)
RETURNS INTEGER AS $$

DECLARE
    v_id_personagem INTEGER;
    v_id_fantasma   INTEGER;

BEGIN
    INSERT INTO public.personagem(id_usuario, nome)
    VALUES (p_id_usuario, p_nome_personagem)
    RETURNING id_personagem INTO v_id_personagem;

    IF p_especie_personagem = 'Zoiudo' THEN
        -- Cria fantasma associado e vincula ao personagem Zoiúdo
        INSERT INTO public.fantasma DEFAULT VALUES
        RETURNING id_fantasma INTO v_id_fantasma;
        INSERT INTO public.ZOIUDO(id_personagem, id_fantasma)
        VALUES (v_id_personagem, v_id_fantasma);
    ELSIF p_especie_personagem = 'Draconico' THEN
        INSERT INTO public.DRACONICO(id_personagem) VALUES (v_id_personagem);
    ELSIF p_especie_personagem = 'Espiritualista' THEN
        INSERT INTO public.ESPIRITUALISTA(id_personagem) VALUES (v_id_personagem);
    ELSIF p_especie_personagem = 'Titan' THEN
        INSERT INTO public.TITAN(id_personagem) VALUES (v_id_personagem);
    ELSE
        RAISE EXCEPTION 'Espécie de personagem não reconhecida: %', p_especie_personagem;
    END IF;

    RETURN v_id_personagem;
END;
$$ LANGUAGE plpgsql;