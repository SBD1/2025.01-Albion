CREATE OR REPLACE FUNCTION f_atualiza_id_fantasma_zoiudo(
    p_id_zoiudo INTEGER,
    p_novo_id_fantasma INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.zoiudo
    SET id_fantasma = p_novo_id_fantasma
    WHERE id_zoiudo = p_id_zoiudo;
END;
$$ LANGUAGE