CREATE OR REPLACE FUNCTION f_deleta_personagem(
    p_id_personagem INTEGER
)
RETURNS VOID AS $$
BEGIN
    DELETE FROM public.personagem
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;
