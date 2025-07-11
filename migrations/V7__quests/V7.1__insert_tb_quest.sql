-- Insert quests for NPCs
INSERT INTO
    QUEST (
        id_npc,
        objetivo,
        nivel_minimo
    )
VALUES (
        (
            SELECT id_npc
            FROM NPC_UNICO
            WHERE
                nome = 'John Mercador'
        ),
        'Minhas rotas comerciais estão sendo constantemente atacadas pelos globins da Floresta do Leste. Esses pequenos saqueadores têm impedido meus carregamentos de mercadorias valiosas. Preciso que você elimine 15 globins para mostrar quem manda! Feito isso, lhe garantirei uma recompensa em ouro',
        15
    ),
    (
        (
            SELECT id_npc
            FROM NPC_UNICO
            WHERE
                nome = 'Aeliana'
        ),
        'Aventureiro, tive visões perturbadoras sobre o Pântano Sombrio. O Devorador de Almas está corrompendo o equilíbrio espiritual da região, sugando a essência vital da terra. Este antigo slime foi transformado por energias profanas e agora ameaça estender sua corrupção para além do pântano. Você deve enfrentá-lo e eliminá-lo antes que seu poder cresça ainda mais. A Igreja da Luz recompensará sua bravura com artefatos de luz',
        20
    ), -- lembrar de criar o item artefato de lux
    (
        (
            SELECT id_npc
            FROM NPC_UNICO
            WHERE
                nome = 'Faelar Bosquevir'
        ),
        'As árvores da Floresta do Leste falam comigo, contando histórias de terror sobre os trolls que desceram da Montanha Nevada. Eles estão destruindo nossos bosques sagrados para construir armas primitivas. Elimine 8 trolls invasores para restaurar o equilíbrio natural da floresta. Irei te recompensar com uma armadura de couro de troll',
        5
    ), --criar armadura couro de troll
    (
        (
            SELECT id_npc
            FROM NPC_UNICO
            WHERE
                nome = 'Thrain Ferreiro'
        ),
        'Os golens das Ruínas Antigas guardam segredos de metalurgia que revolucionariam meu trabalho! Essas construções de pedra contêm núcleos de um metal celestial que a Igreja da Luz usava em tempos antigos. Derrote 12 golens que irei coletar os materiais e forjar para você uma arma lendária imbuída com o poder da luz divina, capaz de atravessar as defesas mais formidáveis!',
        8
    ), -- lembrar de criar o item espada especial
    (
        (
            SELECT id_npc
            FROM NPC_UNICO
            WHERE
                nome = 'Vek''thor O Amaldiçoado'
        ),
        'Meu sangue ferve de ódio pelo Conde Nocturnus, que domina a Caverna Sombria. Outrora fomos irmãos no Culto das Sombras, mas ele me traiu e tentou sugar minha essência vampírica. Agora governa com punho de ferro, impedindo que o Culto realize seus verdadeiros propósitos. Destrua esse tirano para mim, aventureiro. Se conseguir eliminá-lo, irei te recompensar com o conhecimento de uma grande magia das trevas',
        10
    );
-- lembrar de criar tabela magia

-- Função para criar instância de quest
CREATE OR REPLACE FUNCTION criar_instancia_quest(
    p_id_quest INTEGER,
    p_id_personagem INTEGER
) RETURNS VOID AS $$
BEGIN
    -- Verifica se o personagem tem nível suficiente
    IF EXISTS (
        SELECT 1 
        FROM QUEST q 
        JOIN PERSONAGEM p ON p.nivel >= q.nivel_minimo
        WHERE q.id_quest = p_id_quest 
        AND p.id_personagem = p_id_personagem
    ) THEN
        -- Cria a instância da quest
        INSERT INTO INSTANCIA_QUEST (id_quest, id_personagem, quest_status)
        VALUES (p_id_quest, p_id_personagem, FALSE);
    ELSE
        RAISE EXCEPTION 'Personagem não tem nível suficiente para esta quest';
    END IF;
END;
$$ LANGUAGE plpgsql;