INSERT INTO 
    public.NPC(
        especie,id_sala,tipo
        VALUES 
    (   
        'yeti-pé-pequeno',
        (select id_sala 
            from SALA
            WHERE nome = 'Campos Congelados'),
        'GENERICO'        
    ),
    (
        'antigo_explorador',
        (
            select id_sala
                from SALA
                where nome = 'Ruínas Antigas');
        'GENERICO'
    ),
    (
        'aranha-esmaga-ossos',
        (select id_sala
                from SALA
                where nome = 'Caverna Sombria'),
        'GENERICO'
    ),
    (
        'múmias-troca-peles',
        (select id_sala
                from SALA
                where nome = 'Deserto Escaldante'),
        'GENERICO'
    ),
    (
        'blob-a-geleia',
        (select id_sala
                from SALA
                where nome = 'Pântano Sombrio'),
        'GENERICO'
    ),
    (
        'Coruja-das-Geadas',
        (select id_sala
                from SALA
                where nome = 'Montanha Nevada'),
        'GENERICO'
    ),
    (
        'pixies',
        (select id_sala
                from SALA
                where nome = 'Floresta do Leste'),
        'GENERICO'
    ),
    (
        'espiritos-esquecidos',
        (select id_sala
                from SALA
                where nome = 'Ruínas Antigas'),
        'GENERICO'
    ),
    (
        'serpes-flamejantes',
        (select id_sala
                from SALA
                where nome = 'Cânion Vermelho'),
        'GENERICO'
    ),
    (
        'sereias',
        (select id_sala
                from SALA
                where nome = 'Costa Nebulosa'),
        'GENERICO'
    ),
    (
        ' Nimbragos', --Espíritos errantes da névoa, feitos de sombras e vento frio. Sussurram memórias perdidas e enlouquecem viajantes solitários.
        (select id_sala
                from SALA
                where nome = 'Costa Nebulosa'),
        'GENERICO'
    ),
    --npc amigavel
    (
        'humanoide',
        (select id_sala
            from SALA
            where nome = 'Praça Central'),
        'UNICO'
    ),
    (
        'espiritualista',
        (select id_sala
            from SALA
            where nome = 'Praça Central'),
        'UNICO'
    ),
    (
        'elfa',
        (select id_sala
            from SALA
            where nome = 'Praça Central'),
        'UNICO'
    ),
    (
        'humano',
        (select id_sala
            from SALA
            where nome = 'Praça Central'),
        'UNICO'
    ),
    (
        'vampiro',
        (select id_sala
            from SALA
            where nome = 'Praça Central'),
        'UNICO'
    ),
    (
        'meio zoiudo meio vampiro', --npc pseudo-amigavel que vive em outro lugar (Culto das Sombras)
        (select id_sala
            from SALA
            where nome = 'Ruínas Antigas'),
        'UNICO'
    ),
    (
        'criatura lumiar', --npc pseudo-amigavel que vive em outro lugar (Igreja da Luz)
        (select id_sala
            from SALA
            where nome = 'Costa Nebulosa'), 
        'UNICO'
    ),
    --boss
    (
        'a Dama do Lamento Eterno',
        (select id_sala
            from SALA
            where nome = 'Pântano Sombrio'),
        'UNICO'    
            
        
    ),
    (
        'o Gigante dos Picos Gélidos',
        (select id_sala
            from SALA
            where nome = 'Ruínas Antigas'),
        'UNICO'
    ),
    (
        'o Fragmento da Realidade',
        (select id_sala
            from SALA
            where nome = 'Costa Nebulosa'),
        'UNICO'
    )
    );
INSERT INTO 
    public.NPC_UNICO(
    id_npc,nome,tipo
    VALUES
    (
        (select id_npc
            from NPC
            where especie = 'humanoide'),
        'John',
        'AMIGAVEL'
    ),
    (
        (select id_npc
            from NPC
            where especie = 'espiritualista'),
        'Crono',
        'AMIGAVEL'
    ),
    (
        (select id_npc
            from NPC
            where especie = 'elfa'),
        'Ayla',
        'AMIGAVEL'
    ),
    (
        (select id_npc
            from NPC
            where especie = 'humano'),
        'Beren',
        'AMIGAVEL'
    ),
    (
        (select id_npc
            from NPC
            where especie = 'vampiro'),
        'Caliane',
        'AMIGAVEL'
    ), 
    (
        (select id_npc
            from NPC
            where especie = 'meio zoiudo meio vampiro'),
        'Orynth',
        'AMIGAVEL'
    ),
    (
        (select id_npc
            from NPC
            where especie = 'criatura lumiar'),
        'Tho’mek',
        'AMIGAVEL'
    ),
    (
        (select id_npc
            from NPC
            where especie = 'a Dama do Lamento Eterno'),
        'Kirei',
        'BOSS'
    ),
    (
        (select id_npc
            from NPC
            where especie = 'o Gigante dos Picos Gélidos'),
        'Skjaldur',
        'BOSS'
    ),
    (
        (select id_npc
            from NPC
            where especie = 'o Fragmento da Realidade'),
        'SAel`zun',
        'BOSS'
    ),
);
INSERT INTO 
    public.NPC_BOSS(
        id_npc,xp,vida_maxima,vida_atual,ataque_fisico,ataque_magico,defesa_fisica,defesa_magica
        (
            (select id_npc
                from NPC
                where especie = 'a Dama do Lamento Eterno'),
            250,
            15000,
            15000,
            10, --porcentagem?
            70,
            30,
            60
        ),
        (
            (select id_npc
                from NPC
                where especie = 'o Gigante dos Picos Gélidos'),
            250,
            25000,
            25000,
            90,
            5,
            80,
            12
        ),
                (
            (select id_npc
                from NPC
                where especie = 'o Fragmento da Realidade'),
            500,
            100000,
            100000,
            70,
            100,
            100,
            100
        )
    );
