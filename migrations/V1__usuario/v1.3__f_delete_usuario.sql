CREATE OR REPLACE FUNCTION f_deleta_usuario(
    p_username VARCHAR
)
RETURNS VOID AS $$
BEGIN
    DELETE FROM public.usuario
    WHERE username = p_username;
END;
$$ LANGUAGE plpgsql;