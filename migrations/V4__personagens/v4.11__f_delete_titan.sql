CREATE OR REPLACE FUNCTION f_deleta_titan(
    p_id_titan INTEGER
)
RETURNS VOID AS $$
BEGIN
    DELETE FROM public.titan
    WHERE id_titan = p_id_titan;
END;
$$