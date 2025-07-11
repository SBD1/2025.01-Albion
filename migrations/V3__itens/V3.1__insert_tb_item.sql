INSERT INTO
    public.ITEM (
        nome,
        descricao,
        nivel,
        tipo_item
    )
VALUES (
        'Espada de Madeira',
        'Uma espada simples feita de madeira.',
        1,
        'Equipavel'
    ),
    (
        'Espada de Ferro',
        'Uma espada resistente feita de ferro.',
        10,
        'Equipavel'
    ),
    (
        'Espada de Mithril',
        'Uma espada leve e afiada feita de mithril.',
        15,
        'Equipavel'
    ),
    (
        'Espada de Adamantium',
        'Uma espada extremamente poderosa feita de adamantium.',
        20,
        'Equipavel'
    ),
    (
        'Peitoral de Madeira',
        'Proteção básica feita de madeira.',
        1,
        'Equipavel'
    ),
    (
        'Peitoral de Ferro',
        'Proteção robusta feita de ferro.',
        10,
        'Equipavel'
    ),
    (
        'Peitoral de Mithril',
        'Proteção leve e resistente feita de mithril.',
        15,
        'Equipavel'
    ),
    (
        'Peitoral de Adamantium',
        'Proteção impenetrável feita de adamantium.',
        20,
        'Equipavel'
    ),
    (
        'Colar da Serenidade',
        'Um colar que emite uma aura de calma e concentração.',
        1,
        'Equipavel'
    ),
    (
        'Coroa do Imperador',
        'Uma coroa que aumenta o poder mágico de seu portador.',
        10,
        'Equipavel'
    ),
    (
        'Orbe do Destino',
        'Um orbe que permite vislumbrar o futuro e amplifica magia.',
        15,
        'Equipavel'
    ),
    (
        'Grimório Arcano',
        'Um livro mágico que contém feitiços antigos e poderosos.',
        20,
        'Equipavel'
    ),
    (
        'Capacete de Madeira',
        'Proteção básica para a cabeça feita de madeira.',
        1,
        'Equipavel'
    ),
    (
        'Capacete de Ferro',
        'Proteção robusta para a cabeça feita de ferro.',
        10,
        'Equipavel'
    ),
    (
        'Capacete de Mithril',
        'Proteção leve e resistente feita de mithril.',
        15,
        'Equipavel'
    ),
    (
        'Capacete de Adamantium',
        'Proteção impenetrável para a cabeça feita de adamantium.',
        20,
        'Equipavel'
    ),
    (
        'Escudo de Madeira',
        'Um escudo leve feito de madeira resistente.',
        1,
        'Equipavel'
    ),
    (
        'Escudo de Ferro',
        'Um escudo robusto feito de ferro.',
        10,
        'Equipavel'
    ),
    (
        'Escudo de Mithril',
        'Um escudo leve e resistente feito de mithril.',
        15,
        'Equipavel'
    ),
    (
        'Escudo de Adamantium',
        'Um escudo impenetrável feito de adamantium.',
        20,
        'Equipavel'
    ),
    (
        'Fruta Silvestre',
        'Uma fruta pequena e doce encontrada na floresta.',
        1,
        'Nao-Equipavel'
    ),
    (
        'Pão de Centeio',
        'Um pão feito com grãos integrais, rico em energia.',
        10,
        'Nao-Equipavel'
    ),
    (
        'Carne de Caça',
        'Carne suculenta obtida de animais selvagens.',
        15,
        'Nao-Equipavel'
    ),
    (
        'Banquete Épico',
        'Uma refeição completa que restaura energia e vitalidade.',
        20,
        'Nao-Equipavel'
    ),
    (
        'Poção de Mana Fraca',
        'Restaura uma pequena quantidade de mana.',
        1,
        'Nao-Equipavel'
    ),
    (
        'Poção de Mana Média',
        'Restaura uma quantidade moderada de mana.',
        10,
        'Nao-Equipavel'
    ),
    (
        'Poção de Mana Forte',
        'Restaura uma grande quantidade de mana.',
        15,
        'Nao-Equipavel'
    ),
    (
        'Elixir Arcano',
        'Restaura tremenda quantidade de mana.',
        20,
        'Nao-Equipavel'
    );

INSERT INTO
    public.EQUIPAVEL (
        id_item,
        durabilidade_maxima,
        tipo_equipavel
    )
VALUES (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Espada de Madeira'
        ),
        50,
        'Arma'
    ), -- Espada de Madeira
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Espada de Ferro'
        ),
        100,
        'Arma'
    ), -- Espada de Ferro
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Espada de Mithril'
        ),
        150,
        'Arma'
    ), -- Espada de Mithril
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Espada de Adamantium'
        ),
        200,
        'Arma'
    ), -- Espada de Adamantium
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Peitoral de Madeira'
        ),
        50, -- Durabilidade máxima correta
        'Armadura'
    ), -- Peitoral de Madeira
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Peitoral de Ferro'
        ),
        100,
        'Armadura'
    ), -- Peitoral de Ferro
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Peitoral de Mithril'
        ),
        150,
        'Armadura'
    ), -- Peitoral de Mithril
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Peitoral de Adamantium'
        ),
        200,
        'Armadura'
    ), -- Peitoral de Adamantium
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Colar da Serenidade'
        ),
        50,
        'Artefato'
    ), -- Colar da Serenidade
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Coroa do Imperador'
        ),
        100,
        'Artefato'
    ), -- Coroa do Imperador
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Orbe do Destino'
        ),
        150,
        'Artefato'
    ), -- Orbe do Destino
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Grimório Arcano'
        ),
        200,
        'Artefato'
    ), -- Grimório Arcano
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Capacete de Madeira'
        ),
        50,
        'Armadura'
    ), -- Capacete de Madeira
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Capacete de Ferro'
        ),
        100,
        'Armadura'
    ), -- Capacete de Ferro
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Capacete de Mithril'
        ),
        150,
        'Armadura'
    ), -- Capacete de Mithril
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Capacete de Adamantium'
        ),
        200,
        'Armadura'
    ), -- Capacete de Adamantium
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Escudo de Madeira'
        ),
        50,
        'Armadura'
    ), -- Escudo de Madeira
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Escudo de Ferro'
        ),
        100,
        'Armadura'
    ), -- Escudo de Ferro
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Escudo de Mithril'
        ),
        150,
        'Armadura'
    ), -- Escudo de Mithril
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Escudo de Adamantium'
        ),
        200,
        'Armadura'
    );
-- Escudo de Adamantium

INSERT INTO
    public.ARMA (
        id_item,
        aumento_ataque_fisico
    )
VALUES (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Espada de Madeira'
        ),
        10
    ), -- Espada de Madeira
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Espada de Ferro'
        ),
        20
    ), -- Espada de Ferro
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Espada de Mithril'
        ),
        35
    ), -- Espada de Mithril
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Espada de Adamantium'
        ),
        50
    );
-- Espada de Adamantium

INSERT INTO
    public.ARMADURA (
        id_item,
        aumento_defesa_fisica,
        aumento_defesa_magica,
        aumento_vida_maxima
    )
VALUES (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Peitoral de Madeira'
        ),
        5,
        2,
        20
    ), -- Peitoral de Madeira
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Peitoral de Ferro'
        ),
        10,
        5,
        50
    ), -- Peitoral de Ferro
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Peitoral de Mithril'
        ),
        15,
        10,
        100
    ), -- Peitoral de Mithril
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Peitoral de Adamantium'
        ),
        20,
        15,
        150
    ), -- Peitoral de Adamantium
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Capacete de Madeira'
        ),
        5,
        2,
        15
    ), -- Capacete de Madeira
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Capacete de Ferro'
        ),
        10,
        5,
        30
    ), -- Capacete de Ferro
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Capacete de Mithril'
        ),
        15,
        10,
        60
    ), -- Capacete de Mithril
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Capacete de Adamantium'
        ),
        20,
        15,
        100
    ), -- Capacete de Adamantium
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Escudo de Madeira'
        ),
        8,
        3,
        20
    ), -- Escudo de Madeira
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Escudo de Ferro'
        ),
        12,
        6,
        40
    ), -- Escudo de Ferro
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Escudo de Mithril'
        ),
        18,
        12,
        80
    ), -- Escudo de Mithril
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Escudo de Adamantium'
        ),
        25,
        20,
        120
    );
-- Escudo de Adamantium

INSERT INTO
    public.ARTEFATO (
        id_item,
        aumento_ataque_magico,
        aumento_mana_maxima
    )
VALUES (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Colar da Serenidade'
        ),
        10,
        30
    ), -- Colar da Serenidade
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Coroa do Imperador'
        ),
        20,
        60
    ), -- Coroa do Imperador
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Orbe do Destino'
        ),
        30,
        100
    ), -- Orbe do Destino
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Grimório Arcano'
        ),
        50,
        150
    );
-- Grimório Arcano

INSERT INTO
    public.NEQUIPAVEL (id_item, tipo_nequipavel)
VALUES (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Fruta Silvestre'
        ),
        'Comida'
    ), -- Fruta Silvestre
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Pão de Centeio'
        ),
        'Comida'
    ), -- Pão de Centeio
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Carne de Caça'
        ),
        'Comida'
    ), -- Carne de Caça
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Banquete Épico'
        ),
        'Comida'
    ), -- Banquete Épico
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Poção de Mana Fraca'
        ),
        'Pocao'
    ), -- Poção de Mana Fraca
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Poção de Mana Média'
        ),
        'Pocao'
    ), -- Poção de Mana Média
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Poção de Mana Forte'
        ),
        'Pocao'
    ), -- Poção de Mana Forte
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Elixir Arcano'
        ),
        'Pocao'
    );
-- Elixir Arcano

INSERT INTO
    public.COMIDA (
        id_item,
        aumento_vida_atual,
        aumento_stamina_atual
    )
VALUES (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Fruta Silvestre'
        ),
        10,
        5
    ), -- Fruta Silvestre
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Pão de Centeio'
        ),
        20,
        10
    ), -- Pão de Centeio
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Carne de Caça'
        ),
        50,
        20
    ), -- Carne de Caça
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Banquete Épico'
        ),
        100,
        50
    );
-- Banquete Épico

INSERT INTO
    public.POCAO (id_item, aumento_mana_atual)
VALUES (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Poção de Mana Fraca'
        ),
        15
    ), -- Poção de Mana Fraca
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Poção de Mana Média'
        ),
        30
    ), -- Poção de Mana Média
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Poção de Mana Forte'
        ),
        60
    ), -- Poção de Mana Forte
    (
        (
            SELECT id_item
            FROM public.ITEM
            WHERE
                nome = 'Elixir Arcano'
        ),
        120
    );
-- Elixir Arcano