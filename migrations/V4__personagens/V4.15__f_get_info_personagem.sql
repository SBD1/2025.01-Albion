CREATE OR REPLACE FUNCTION f_get_info_personagem(
    p_id_personagem INTEGER
)
RETURNS TABLE (
    nome VARCHAR,
    nivel INTEGER,
    qtd_ouro INTEGER,
    exp_maxima INTEGER,
    exp_atual INTEGER,
    vida_atual INTEGER,
    vida_maxima INTEGER,
    stamina_atual INTEGER,
    stamina_maxima INTEGER,
    ataque_fisico INTEGER,
    defesa_fisica INTEGER,
    defesa_magica INTEGER,
    classe TEXT,
    -- Atributos específicos do Zoiudo (Fantasma)
    nome_fantasma VARCHAR,
    nivel_fantasma INTEGER,
    exp_maxima_fantasma INTEGER,
    exp_atual_fantasma INTEGER,
    vida_maxima_fantasma INTEGER,
    vida_atual_fantasma INTEGER,
    ataque_fisico_fantasma INTEGER,
    ataque_magico_fantasma INTEGER,
    defesa_fisica_fantasma INTEGER,
    defesa_magica_fantasma INTEGER,
    -- Atributos específicos do Espiritualista
    mana_total INTEGER,
    mana_atual INTEGER,
    ataque_magico_espiritualista INTEGER,
    -- Atributos específicos do Draconico
    custo_stamina INTEGER,
    aumento_vida_atual INTEGER,
    aumento_ataque_fisico INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        p.nome,
        p.nivel,
        p.qtd_ouro,
        p.exp_maxima,
        p.exp_atual,
        p.vida_atual,
        p.vida_maxima,
        p.stamina_atual,
        p.stamina_maxima,
        p.ataque_fisico,
        p.defesa_fisica,
        p.defesa_magica,
        CASE 
            WHEN z.id_personagem IS NOT NULL THEN 'Zoiudo'
            WHEN e.id_personagem IS NOT NULL THEN 'Espiritualista'
            WHEN d.id_personagem IS NOT NULL THEN 'Draconico'
            WHEN t.id_personagem IS NOT NULL THEN 'Titan'
            ELSE 'Desconhecido'
        END AS classe,
        -- Atributos do Fantasma (para Zoiudo)
        f.nome AS nome_fantasma,
        f.nivel AS nivel_fantasma,
        f.exp_maxima AS exp_maxima_fantasma,
        f.exp_atual AS exp_atual_fantasma,
        f.vida_maxima AS vida_maxima_fantasma,
        f.vida_atual AS vida_atual_fantasma,
        f.ataque_fisico AS ataque_fisico_fantasma,
        f.ataque_magico AS ataque_magico_fantasma,
        f.defesa_fisica AS defesa_fisica_fantasma,
        f.defesa_magica AS defesa_magica_fantasma,
        -- Atributos do Espiritualista
        e.mana_total,
        e.mana_atual,
        e.ataque_magico AS ataque_magico_espiritualista,
        -- Atributos do Draconico
        d.custo_stamina,
        d.aumento_vida_atual,
        d.aumento_ataque_fisico
    FROM 
        public.PERSONAGEM p
        LEFT JOIN public.ZOIUDO z ON p.id_personagem = z.id_personagem
        LEFT JOIN public.FANTASMA f ON z.id_fantasma = f.id_fantasma
        LEFT JOIN public.ESPIRITUALISTA e ON p.id_personagem = e.id_personagem
        LEFT JOIN public.DRACONICO d ON p.id_personagem = d.id_personagem
        LEFT JOIN public.TITAN t ON p.id_personagem = t.id_personagem
    WHERE 
        p.id_personagem = p_id_personagem;
END;
$$ LANGUAGE plpgsql;