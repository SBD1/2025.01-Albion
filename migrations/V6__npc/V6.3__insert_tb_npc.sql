-- NPCs Genéricos (Mobs)

-- Yeti (Campos Congelados)
SELECT criar_npc_generico (
        'Yeti', 'Campos Congelados', 100, -- XP
        250, -- Vida Máxima (criatura resistente)
        70, -- Ataque Físico (força bruta)
        10, -- Ataque Mágico (pouca aptidão mágica)
        60, -- Defesa Física (pelagem grossa)
        30 -- Defesa Mágica (vulnerável a magias)
    );

-- Vampiro (Caverna Sombria)
SELECT criar_npc_generico (
        'Vampiro', 'Caverna Sombria', 120, -- XP
        150, -- Vida Máxima 
        40, -- Ataque Físico 
        85, -- Ataque Mágico (habilidades de sangue/sombra)
        35, -- Defesa Física 
        65 -- Defesa Mágica (resistência a magias)
    );

-- Múmia (Deserto Escaldante)
SELECT criar_npc_generico (
        'Múmia', 'Deserto Escaldante', 90, -- XP
        180, -- Vida Máxima (resistência ancestral)
        50, -- Ataque Físico 
        60, -- Ataque Mágico (maldições)
        55, -- Defesa Física (bandagens endurecidas)
        40 -- Defesa Mágica (vulnerável a magias de água)
    );

-- Slime-Corrompido (Pântano Sombrio)
SELECT criar_npc_generico (
        'Slime-Corrompido', 'Pântano Sombrio', 70, -- XP
        120, -- Vida Máxima 
        30, -- Ataque Físico 
        65, -- Ataque Mágico (ácido/corrosão)
        50, -- Defesa Física (corpo gelatinoso)
        50 -- Defesa Mágica (resistente a magias)
    );

-- Troll (Montanha Nevada)
SELECT criar_npc_generico (
        'Troll', 'Montanha Nevada', 150, -- XP
        300, -- Vida Máxima (regeneração)
        85, -- Ataque Físico (força bruta)
        5, -- Ataque Mágico (quase nulo)
        70, -- Defesa Física (pele dura)
        10 -- Defesa Mágica (vulnerável a magias)
    );

-- Globin (Floresta do Leste)
SELECT criar_npc_generico (
        'Globin', 'Floresta do Leste', 50, -- XP
        50, -- Vida Máxima (criatura pequena)
        45, -- Ataque Físico (armas primitivas)
        25, -- Ataque Mágico (pouca magia)
        30, -- Defesa Física 
        30 -- Defesa Mágica 
    );

-- Golem (Ruínas Antigas)
SELECT criar_npc_generico (
        'Golem', 'Ruínas Antigas', 200, -- XP
        350, -- Vida Máxima (construção robusta)
        90, -- Ataque Físico (corpo de pedra)
        35, -- Ataque Mágico (runas antigas)
        80, -- Defesa Física (matéria mineral)
        45 -- Defesa Mágica (encantamentos fracos)
    );

------------------------------------------------------------------------------------------------

-- NPC AMIGAVEIS

-- Humano (Praça Central - Igreja da Luz)
SELECT criar_npc_unico_amigavel (
        'Humano', 'Praça Central', 'John Mercador', -- Nome único
        NULL
    );

-- Espiritualista (Praça Central - Igreja da Luz)
SELECT criar_npc_unico_amigavel (
        'Espiritualista', 'Praça Central', 'Aeliana', -- Nome único
        'Igreja da Luz'
    );

-- Elfo (Praça Central - Igreja da Luz)
SELECT criar_npc_unico_amigavel (
        'Elfo', 'Praça Central', 'Faelar Bosquevir', -- Nome único
        NULL
    );

-- Segundo Humano (Praça Central - Igreja da Luz)
SELECT criar_npc_unico_amigavel (
        'Humano', 'Praça Central', 'Thrain Ferreiro', -- Nome único
        NULL
    );

-- Meio Zoiudo Meio Vampiro (Ruínas Antigas - Culto das Sombras)
SELECT criar_npc_unico_amigavel (
        'Meio Zoiudo Meio Vampiro', 'Ruínas Antigas', 'Vek''thor O Amaldiçoado', -- Nome único
        'Culto das Sombras'
    );

-----------------------------------------------------------------------------------------------------------

-- NPCs BOSS

-- Versão alternativa mantendo espécies originais
SELECT criar_npc_unico_boss (
        'Slime-Corrompido', 'Pântano Sombrio', 'O Devorador de Almas', 500, 15000, 30, 150, 50, 120
    );

SELECT criar_npc_unico_boss (
        'Vampiro', 'Caverna Sombria', 'Conde Nocturnus', 700, 18000, 90, 200, 80, 180
    );

SELECT criar_npc_unico_boss (
        'Troll', 'Montanha Nevada', 'Trundle Rugido de Gelo', 800, 30000, 250, 20, 200, 50
    );