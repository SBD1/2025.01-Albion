-- Função para atualizar a senha de um usuário
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