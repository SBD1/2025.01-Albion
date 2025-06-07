CREATE OR REPLACE FUNCTION f_registra_usuario(
    p_username VARCHAR,
    p_senha    VARCHAR)
RETURNS INTEGER AS $$

DECLARE
    v_id INTEGER;

BEGIN
    INSERT INTO usuario(username, senha)
    VALUES (p_username, p_senha)
    RETURNING id_usuario INTO v_id;

    RETURN v_id;
END;
$$ LANGUAGE plpgsql;