
INSERT INTO
    public.MAGIA (
        nome,
        descricao,
        nivel_requerido,
        custo_mana,
        dano_base,
        cura_base
    )
VALUES (
        'Toque Espiritual',
        'Canaliza energia espiritual através das mãos para causar dano direto ao inimigo.',
        1,
        15,
        25,
        0
    ),
    (
        'Lança Ectoplásmica',
        'Materializa uma lança sólida de ectoplasma que perfura armaduras inimigas.',
        5,
        35,
        40,
        0
    ),
 (
        'Cura Espiritual',
        'Canaliza energia vital positiva para restaurar pontos de vida.',
        5,
        20,
        0,
        50
    ),

    (
        'Apocalipse Cósmico',
        'Invoca uma explosão massiva de energia espiritual que devasta a área ao redor.',
        10,
        150,
        120,
        0
    ),
    (
        'Vampirismo Espiritual',
        'Drena energia vital do inimigo causando dano e ao mesmo tempo cura o conjurador.',
        20,
        100,
        150,
        100
    );
