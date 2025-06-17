-- Atualizar turnos_maximo_dragao
CREATE OR REPLACE FUNCTION f_atualiza_turnos_maximo_dragao_draconico(
    p_id_draconico INTEGER,
    p_novo_turnos_maximo_dragao INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.draconico
    SET turnos_maximo_dragao = p_novo_turnos_maximo_dragao
    WHERE id_draconico = p_id_draconico;
END;
$$ LANGUAGE plpgsql;

-- Atualizar turnos_atual_dragao
CREATE OR REPLACE FUNCTION f_atualiza_turnos_atual_dragao_draconico(
    p_id_draconico INTEGER,
    p_novo_turnos_atual_dragao INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.draconico
    SET turnos_atual_dragao = p_novo_turnos_atual_dragao
    WHERE id_draconico = p_id_draconico;
END;
$$ LANGUAGE plpgsql;

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