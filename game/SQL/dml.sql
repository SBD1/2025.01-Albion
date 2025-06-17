--TABELA USUÁRIO

CREATE OR REPLACE FUNCTION f_registra_usuario(
    p_username VARCHAR,
    p_senha    VARCHAR)
RETURNS INTEGER AS $$

DECLARE
    v_id INTEGER;

BEGIN
    INSERT INTO public.usuario(username, password)
    VALUES (p_username, p_senha)
    RETURNING id_usuario INTO v_id;

    RETURN v_id;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION f_atualiza_usuario(
    p_username VARCHAR,
    p_nova_senha VARCHAR
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.usuario
    SET password = p_nova_senha
    WHERE username = p_username;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION f_deleta_usuario(
    p_username VARCHAR
)
RETURNS VOID AS $$
BEGIN
    DELETE FROM public.usuario
    WHERE username = p_username;
END;
$$ LANGUAGE plpgsql;

