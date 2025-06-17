

-- Tabela Personagem
CREATE OR REPLACE FUNCTION f_atualiza_nome_personagem(
    p_id_personagem INTEGER,
    p_novo_nome VARCHAR
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET nome = p_novo_nome
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION f_atualiza_faccao_personagem(
    p_id_personagem INTEGER,
    p_nova_faccao VARCHAR
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET faccao = p_nova_faccao
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION f_atualiza_nivel_personagem(
    p_id_personagem INTEGER,
    p_novo_nivel INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET nivel = p_novo_nivel
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION f_atualiza_ouro_personagem(
    p_id_personagem INTEGER,
    p_novo_ouro INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET qtd_ouro = p_novo_ouro
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION f_atualiza_exp_maxima_personagem(
    p_id_personagem INTEGER,
    p_nova_exp_maxima INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET exp_maxima = p_nova_exp_maxima
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION f_atualiza_exp_atual_personagem(
    p_id_personagem INTEGER,
    p_nova_exp_atual INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET exp_atual = p_nova_exp_atual
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION f_atualiza_vida_atual_personagem(
    p_id_personagem INTEGER,
    p_nova_vida_atual INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET vida_atual = p_nova_vida_atual
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION f_atualiza_vida_maxima_personagem(
    p_id_personagem INTEGER,
    p_nova_vida_maxima INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET vida_maxima = p_nova_vida_maxima
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION f_atualiza_stamina_atual_personagem(
    p_id_personagem INTEGER,
    p_nova_stamina_atual INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET stamina_atual = p_nova_stamina_atual
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION f_atualiza_stamina_maxima_personagem(
    p_id_personagem INTEGER,
    p_nova_stamina_maxima INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET stamina_maxima = p_nova_stamina_maxima
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION f_atualiza_ataque_fisico_personagem(
    p_id_personagem INTEGER,
    p_novo_ataque_fisico INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET ataque_fisico = p_novo_ataque_fisico
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION f_atualiza_defesa_fisica_personagem(
    p_id_personagem INTEGER,
    p_nova_defesa_fisica INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET defesa_fisica = p_nova_defesa_fisica
    WHERE id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION f_atualiza_defesa_magica_personagem(
    p_id_personagem INTEGER,
    p_nova_defesa_magica INTEGER
)
RETURNS VOID AS $$
BEGIN
    UPDATE public.personagem
    SET defesa_magica = p_nova_defesa_magica