-- Deletar DRACONICO
CREATE OR REPLACE FUNCTION f_deleta_draconico(
    p_id_draconico INTEGER
)
RETURNS VOID AS $$
BEGIN
    DELETE FROM public.draconico
    WHERE id_draconico = p_id_draconico;
END;
$$ LANGUAGE plpgsql;