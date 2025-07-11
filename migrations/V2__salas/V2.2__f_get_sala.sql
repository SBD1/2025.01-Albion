CREATE OR REPLACE FUNCTION f_get_sala(
    p_id_personagem INTEGER)
RETURNS TABLE (
    id_sala INTEGER,
    nome VARCHAR(50)
) AS $$

BEGIN
    RETURN QUERY
    SELECT s.id_sala, s.nome
    FROM public.personagem p
    JOIN public.sala s ON p.id_sala = s.id_sala
    WHERE p.id_personagem = p_id_personagem;
    
END;
$$ LANGUAGE plpgsql;