INSERT INTO
    public.NPC (especie, id_sala, tipo)
VALUES (
        'yeti-pé-pequeno',
        (
            select id_sala
            from public.SALA
            WHERE
                nome = 'Campos Congelados'
        ),
        'GENERICO'
    ),
    (
        'antigo_explorador',
        (
            select id_sala
            from public.SALA
            where
                nome = 'Ruínas Antigas'
        ),
        'GENERICO'
    ),
    (
        'aranha-esmaga-ossos',
        (
            select id_sala
            from public.SALA
            where
                nome = 'Caverna Sombria'
        ),
        'GENERICO'
    ),
    (
        'múmias-troca-peles',
        (
            select id_sala
            from public.SALA
            where
                nome = 'Deserto Escaldante'
        ),
        'GENERICO'
    ),
    (
        'blob-a-geleia',
        (
            select id_sala
            from public.SALA
            where
                nome = 'Pântano Sombrio'
        ),
        'GENERICO'
    ),
    (
        'Coruja-das-Geadas',
        (
            select id_sala
            from public.SALA
            where
                nome = 'Montanha Nevada'
        ),
        'GENERICO'
    ),
    (
        'pixies',
        (
            select id_sala
            from public.SALA
            where
                nome = 'Floresta do Leste'
        ),
        'GENERICO'
    ),
    (
        'espiritos-esquecidos',
        (
            select id_sala
            from public.SALA
            where
                nome = 'Ruínas Antigas'
        ),
        'GENERICO'
    ),
    (
        'serpes-flamejantes',
        (
            select id_sala
            from public.SALA
            where
                nome = 'Cânion Vermelho'
        ),
        'GENERICO'
    ),
    (
        'sereias',
        (
            select id_sala
            from public.SALA
            where
                nome = 'Costa Nebulosa'
        ),
        'GENERICO'
    ),
    (
        'Nimbragos', --Espíritos errantes da névoa, feitos de sombras e vento frio. Sussurram memórias perdidas e enlouquecem viajantes solitários.
        (
            select id_sala
            from public.SALA
            where
                nome = 'Costa Nebulosa'
        ),
        'GENERICO'
    ),
    --npc amigavel
    (
        'humanoide',
        (
            select id_sala
            from public.SALA
            where
                nome = 'Praça Central'
        ),
        'UNICO'
    ),
    (
        'espiritualista',
        (
            select id_sala
            from public.SALA
            where
                nome = 'Praça Central'
        ),
        'UNICO'
    ),
    (
        'elfa',
        (
            select id_sala
            from public.SALA
            where
                nome = 'Praça Central'
        ),
        'UNICO'
    ),
    (
        'humano',
        (
            select id_sala
            from public.SALA
            where
                nome = 'Praça Central'
        ),
        'UNICO'
    ),
    (
        'vampiro',
        (
            select id_sala
            from public.SALA
            where
                nome = 'Praça Central'
        ),
        'UNICO'
    ),
    (
        'meio zoiudo meio vampiro', --npc pseudo-amigavel que vive em outro lugar (Culto das Sombras)
        (
            select id_sala
            from public.SALA
            where
                nome = 'Ruínas Antigas'
        ),
        'UNICO'
    ),
    (
        'criatura lumiar', --npc pseudo-amigavel que vive em outro lugar (Igreja da Luz)
        (
            select id_sala
            from public.SALA
            where
                nome = 'Costa Nebulosa'
        ),
        'UNICO'
    ),
    --boss
    (
        'a Dama do Lamento Eterno',
        (
            select id_sala
            from public.SALA
            where
                nome = 'Pântano Sombrio'
        ),
        'UNICO'
    ),
    (
        'o Gigante dos Picos Gélidos',
        (
            select id_sala
            from public.SALA
            where
                nome = 'Ruínas Antigas'
        ),
        'UNICO'
    ),
    (
        'o Fragmento da Realidade',
        (
            select id_sala
            from public.SALA
            where
                nome = 'Costa Nebulosa'
        ),
        'UNICO'
    );

INSERT INTO
    public.NPC_UNICO (id_npc, nome, tipo)
VALUES (
        (
            select id_npc
            from public.NPC
            where
                especie = 'humanoide'
        ),
        'John',
        'AMIGAVEL'
    ),
    (
        (
            select id_npc
            from public.NPC
            where
                especie = 'espiritualista'
        ),
        'Crono',
        'AMIGAVEL'
    ),
    (
        (
            select id_npc
            from public.NPC
            where
                especie = 'elfa'
        ),
        'Ayla',
        'AMIGAVEL'
    ),
    (
        (
            select id_npc
            from public.NPC
            where
                especie = 'humano'
        ),
        'Beren',
        'AMIGAVEL'
    ),
    (
        (
            select id_npc
            from public.NPC
            where
                especie = 'vampiro'
        ),
        'Caliane',
        'AMIGAVEL'
    ),
    (
        (
            select id_npc
            from public.NPC
            where
                especie = 'meio zoiudo meio vampiro'
        ),
        'Orynth',
        'AMIGAVEL'
    ),
    (
        (
            select id_npc
            from public.NPC
            where
                especie = 'criatura lumiar'
        ),
        'Tho''mek',
        'AMIGAVEL'
    ),
    (
        (
            select id_npc
            from public.NPC
            where
                especie = 'a Dama do Lamento Eterno'
        ),
        'Kirei',
        'BOSS'
    ),
    (
        (
            select id_npc
            from public.NPC
            where
                especie = 'o Gigante dos Picos Gélidos'
        ),
        'Skjaldur',
        'BOSS'
    ),
    (
        (
            select id_npc
            from public.NPC
            where
                especie = 'o Fragmento da Realidade'
        ),
        'SAel`zun',
        'BOSS'
    );

INSERT INTO
    public.NPC_BOSS (
        id_npc,
        xp,
        vida_maxima,
        vida_atual,
        ataque_fisico,
        ataque_magico,
        defesa_fisica,
        defesa_magica
    )
VALUES (
        (
            select id_npc
            from public.NPC
            where
                especie = 'a Dama do Lamento Eterno'
        ),
        250,
        15000,
        15000,
        10, --porcentagem?
        70,
        30,
        60
    ),
    (
        (
            select id_npc
            from public.NPC
            where
                especie = 'o Gigante dos Picos Gélidos'
        ),
        250,
        25000,
        25000,
        90,
        5,
        80,
        12
    ),
    (
        (
            select id_npc
            from public.NPC
            where
                especie = 'o Fragmento da Realidade'
        ),
        500,
        100000,
        100000,
        70,
        100,
        100,
        100
    );

INSERT INTO
    public.NPC_AMIGAVEL (id_npc, faccao)
VALUES (
        (
            select id_npc
            from public.NPC
            where
                especie = 'humanoide'
        ),
        'Culto das Sombras'
    ),
    (
        (
            select id_npc
            from public.NPC
            where
                especie = 'espiritualista'
        ),
        'Igreja da Luz'
    ),
    (
        (
            select id_npc
            from public.NPC
            where
                especie = 'elfa'
        ),
        'Igreja da Luz'
    ),
    (
        (
            select id_npc
            from public.NPC
            where
                especie = 'humano'
        ),
        'Igreja da Luz'
    ),
    (
        (
            select id_npc
            from public.NPC
            where
                especie = 'vampiro'
        ),
        'Culto das Sombras'
    ),
    (
        (
            select id_npc
            from public.NPC
            where
                especie = 'meio zoiudo meio vampiro'
        ),
        'Culto das Sombras'
    ),
    (
        (
            select id_npc
            from public.NPC
            where
                especie = 'criatura lumiar'
        ),
        'Igreja da Luz'
    );

INSERT INTO
    public.NPC_GENERICO (
        id_npc,
        xp,
        vida_maxima,
        ataque_fisico,
        ataque_magico,
        defesa_fisica,
        defesa_magica
    )
VALUES (
        (
            select id_npc
            From public.NPC
            where
                especie = 'yeti-pé-pequeno'
        ),
        100,
        25,
        25,
        25,
        25,
        25
    ),
    (
        (
            select id_npc
            From public.NPC
            where
                especie = 'antigo_explorador'
        ),
        100,
        25,
        25,
        25,
        25,
        25
    ),
    (
        (
            select id_npc
            From public.NPC
            where
                especie = 'aranha-esmaga-ossos'
        ),
        100,
        25,
        25,
        25,
        25,
        25
    ),
    (
        (
            select id_npc
            From public.NPC
            where
                especie = 'múmias-troca-peles'
        ),
        100,
        25,
        25,
        25,
        25,
        25
    ),
    (
        (
            select id_npc
            From public.NPC
            where
                especie = 'blob-a-geleia'
        ),
        100,
        25,
        25,
        25,
        25,
        25
    ),
    (
        (
            select id_npc
            From public.NPC
            where
                especie = 'Coruja-das-Geadas'
        ),
        100,
        25,
        25,
        25,
        25,
        25
    ),
    (
        (
            select id_npc
            From public.NPC
            where
                especie = 'pixies'
        ),
        100,
        25,
        25,
        25,
        25,
        25
    ),
    (
        (
            select id_npc
            From public.NPC
            where
                especie = 'espiritos-esquecidos'
        ),
        100,
        25,
        25,
        25,
        25,
        25
    ),
    (
        (
            select id_npc
            From public.NPC
            where
                especie = 'serpes-flamejantes'
        ),
        100,
        25,
        25,
        25,
        25,
        25
    ),
    (
        (
            select id_npc
            From public.NPC
            where
                especie = 'sereias'
        ),
        100,
        25,
        25,
        25,
        25,
        25
    ),
    (
        (
            select id_npc
            From public.NPC
            where
                especie = 'Nimbragos'
        ),
        100,
        25,
        25,
        25,
        25,
        25
    );