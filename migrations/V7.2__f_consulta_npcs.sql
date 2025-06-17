CREATE OR REPLACE FUNCTION f_consulta_npcs_amigaveis(p_id_sala INTEGER)
RETURNS TABLE (
    id_npc INTEGER,
    nome VARCHAR,
    especie VARCHAR,
    faccao VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        n.id_npc,
        u.nome,
        n.especie,
        a.faccao
    FROM 
        public.NPC n
    JOIN 
        public.NPC_UNICO u ON n.id_npc = u.id_npc
    JOIN 
        public.NPC_AMIGAVEL a ON u.id_npc = a.id_npc
    WHERE 
        n.id_sala = p_id_sala
    ORDER BY 
        u.nome;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION f_consulta_npcs_boss(p_id_sala INTEGER)
RETURNS TABLE (
    id_npc INTEGER,
    nome VARCHAR,
    especie VARCHAR,
    xp INTEGER,
    vida_atual INTEGER,
    vida_maxima INTEGER,
    ataque_fisico INTEGER,
    ataque_magico INTEGER,
    defesa_fisica INTEGER,
    defesa_magica INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        n.id_npc,
        u.nome,
        n.especie,
        b.xp,
        b.vida_atual,
        b.vida_maxima,
        b.ataque_fisico,
        b.ataque_magico,
        b.defesa_fisica,
        b.defesa_magica
    FROM 
        public.NPC n
    JOIN 
        public.NPC_UNICO u ON n.id_npc = u.id_npc
    JOIN 
        public.NPC_BOSS b ON u.id_npc = b.id_npc
    WHERE 
        n.id_sala = p_id_sala;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION f_consulta_npcs_genericos(p_id_sala INTEGER)
RETURNS TABLE (
    id_instancia INTEGER,
    especie VARCHAR,
    xp INTEGER,
    vida_atual INTEGER,
    vida_maxima INTEGER,
    ataque_fisico INTEGER,
    ataque_magico INTEGER,
    defesa_fisica INTEGER,
    defesa_magica INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        i.id_instancia,
        n.especie,
        g.xp,
        i.vida_atual,
        g.vida_maxima,
        g.ataque_fisico,
        g.ataque_magico,
        g.defesa_fisica,
        g.defesa_magica
    FROM 
        public.NPC n
    JOIN 
        public.NPC_GENERICO g ON n.id_npc = g.id_npc
    JOIN 
        public.INSTANCIA_NPC_GENERICO i ON g.id_npc = i.id_npc
    WHERE 
        n.id_sala = p_id_sala
    ORDER BY 
        i.id_instancia;
END;
$$ LANGUAGE plpgsql;