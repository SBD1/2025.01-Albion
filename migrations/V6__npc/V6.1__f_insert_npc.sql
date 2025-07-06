CREATE OR REPLACE FUNCTION criar_npc_generico (
    especie_npc VARCHAR(50),
    nome_sala_npc VARCHAR(50),
    xp_npc INTEGER,
    vida_maxima_npc INTEGER,
    ataque_fisico_npc INTEGER,
    ataque_magico_npc INTEGER,
    defesa_fisica_npc INTEGER,
    defesa_magica_npc INTEGER

) RETURNS VOID AS $$
DECLARE
    sala_id INTEGER;
    npc_id INTEGER;
BEGIN 
    SELECT id_sala INTO sala_id
    FROM SALA WHERE nome = nome_sala_npc;

    INSERT INTO NPC(especie, id_sala, tipo)
    VALUES(especie_npc, sala_id, 'GENERICO')
    RETURNING id_npc INTO npc_id;

    INSERT INTO NPC_GENERICO(
        id_npc, 
        xp, 
        vida_maxima, 
        ataque_fisico, 
        ataque_magico, 
        defesa_fisica, 
        defesa_magica
    )
    VALUES(
        npc_id, 
        xp_npc, 
        vida_maxima_npc, 
        ataque_fisico_npc, 
        ataque_magico_npc, 
        defesa_fisica_npc, 
        defesa_magica_npc
    );
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION criar_npc_unico_boss (
    especie_npc VARCHAR(50),
    nome_sala_npc VARCHAR(50),
    nome_npc VARCHAR(50),
    xp_npc INTEGER,
    vida_maxima_npc INTEGER,
    ataque_fisico_npc INTEGER,
    ataque_magico_npc INTEGER,
    defesa_fisica_npc INTEGER,
    defesa_magica_npc INTEGER
)
RETURNS VOID AS $$
DECLARE
    sala_id INTEGER;
    npc_id INTEGER;
BEGIN 
    SELECT id_sala INTO sala_id 
    FROM SALA WHERE nome = nome_sala_npc;

    INSERT INTO NPC(especie, id_sala, tipo)
    VALUES(especie_npc, sala_id, 'UNICO')
    RETURNING id_npc INTO npc_id;

    INSERT INTO NPC_UNICO(id_npc, nome, tipo)
    VALUES(npc_id, nome_npc, 'BOSS');

    INSERT INTO NPC_BOSS(
        id_npc,
        xp,
        vida_maxima,
        vida_atual,
        ataque_fisico,
        ataque_magico,
        defesa_fisica,
        defesa_magica
    )
    VALUES(
        npc_id,
        xp_npc,
        vida_maxima_npc,
        vida_maxima_npc,
        ataque_fisico_npc,
        ataque_magico_npc,
        defesa_fisica_npc,
        defesa_magica_npc
        );
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION criar_npc_unico_amigavel (
    especie_npc VARCHAR(50),
    nome_sala_npc VARCHAR(50),
    nome_npc VARCHAR(50),
    faccao_npc VARCHAR(20)
)
RETURNS VOID AS $$
DECLARE
    sala_id INTEGER;
    npc_id INTEGER;
BEGIN 
    SELECT id_sala INTO sala_id 
    FROM SALA WHERE nome = nome_sala_npc;

    INSERT INTO NPC(especie, id_sala, tipo)
    VALUES(especie_npc, sala_id, 'UNICO')
    RETURNING id_npc INTO npc_id;

    INSERT INTO NPC_UNICO(id_npc, nome, tipo)
    VALUES(npc_id, nome_npc, 'AMIGAVEL');

    INSERT INTO NPC_AMIGAVEL(id_npc, faccao)
    VALUES(npc_id, faccao_npc);

END;
$$ LANGUAGE plpgsql;

-- Função para criar instância de NPC genérico e retornar id_instancia
CREATE OR REPLACE FUNCTION f_cria_instancia_npc_generico(
    p_id_npc INTEGER
) RETURNS INTEGER AS $$
DECLARE
    new_id INTEGER;
    vida_max INTEGER;
BEGIN
    SELECT vida_maxima INTO vida_max
    FROM public.NPC_GENERICO
    WHERE id_npc = p_id_npc;

    INSERT INTO public.INSTANCIA_NPC_GENERICO(id_npc, vida_atual)
    VALUES (p_id_npc, COALESCE(vida_max, 100))
    RETURNING id_instancia INTO new_id;
    RETURN new_id;
END;
$$ LANGUAGE plpgsql;