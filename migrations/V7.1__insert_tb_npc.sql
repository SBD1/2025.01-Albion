INSERT INTO 
    public.npc(
        especie,id_sala,tipo
        VALUES 
    (   
        'yeti-pé-pequeno',
        (select id_sala 
            from sala
            WHERE nome = 'Campos Congelados'),
        'GENERICO'        
    ),
    (
        'antigo_explorador',
        (
            select id_sala
                from sala
                where nome = 'Ruínas Antigas');
        'GENERICO'
    ),
    (
        'aranha-esmaga-ossos',
        (select id_sala
                from sala
                where nome = 'Caverna Sombria'),
        'GENERICO'
    ),
    (
        'múmias-troca-peles',
        (select id_sala
                from sala
                where nome = 'Deserto Escaldante'),
        'GENERICO'
    ),
    (
        'blob-a-geleia',
        (select id_sala
                from sala
                where nome = 'Pântano Sombrio'),
        'GENERICO'
    ),
    (
        'Coruja-das-Geadas',
        (select id_sala
                from sala
                where nome = 'Montanha Nevada'),
        'GENERICO'
    ),
    (
        'pixies',
        (select id_sala
                from sala
                where nome = 'Floresta do Leste'),
        'GENERICO'
    ),
    (
        'espiritos-esquecidos',
        (select id_sala
                from sala
                where nome = 'Ruínas Antigas'),
        'GENERICO'
    ),
    (
        'serpes-flamejantes',
        (select id_sala
                from sala
                where nome = 'Cânion Vermelho'),
        'GENERICO'
    ),
    (
        'sereias',
        (select id_sala
                from sala
                where nome = 'Costa Nebulosa'),
        'GENERICO'
    ),
    (
        ' Nimbragos', --Espíritos errantes da névoa, feitos de sombras e vento frio. Sussurram memórias perdidas e enlouquecem viajantes solitários.
        (select id_sala
                from sala
                where nome = 'Costa Nebulosa'),
        'GENERICO'
    ),
    

    )