CREATE OR REPLACE FUNCTION f_cria_personagem(
    p_id_usuario      INTEGER,
    p_nome_personagem VARCHAR)
RETURNS INTEGER AS $$

DECLARE
    v_id_personagem INTEGER;

BEGIN
    INSERT INTO public.personagem(id_usuario, nome)
    VALUES (p_id_usuario, p_nome_personagem)
    RETURNING id_personagem INTO v_id_personagem;

    RETURN v_id_personagem;
END;
$$ LANGUAGE plpgsql;