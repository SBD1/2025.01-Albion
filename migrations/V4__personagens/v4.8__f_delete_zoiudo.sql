-- Deletar ZOIUDO
CREATE OR REPLACE FUNCTION f_deleta_zoiudo(
    p_id_zoiudo INTEGER
)
RETURNS VOID AS $$
BEGIN
    DELETE FROM public.zoiudo
    WHERE id_zoiudo = p_id_zoiudo;
END;
$$ LANGUAGE plpgsql;


