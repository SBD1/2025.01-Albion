-- Atualizar aumento_ataque_fisico
CREATE OR REPLACE FUNCTION f_atualiza_aumento_ataque_fisico_draconico(
    p_id_draconico INTEGER,
    p_novo_aumento_ataque_fisico INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.draconico
    SET aumento_ataque_fisico = p_novo_aumento_ataque_fisico
    WHERE id_draconico = p_id_draconico;
END;
$$ LANGUAGE plpgsql;