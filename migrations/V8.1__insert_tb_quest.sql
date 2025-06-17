-- Insert quests for NPCs
INSERT INTO QUEST (id_npc, objetivo, nivel_minimo) VALUES
-- Orynth's Quest (Special NPC from Ancient Ruins)
(1, 'Orynth, o misterioso habitante das Ruínas Antigas, busca ajuda para decifrar antigos pergaminhos que podem revelar a verdade sobre sua natureza vampírica. Ele acredita que os textos contêm pistas sobre como controlar sua sede de sangue e encontrar um equilíbrio entre sua humanidade e sua condição. A missão envolve explorar as ruínas mais profundas, enfrentar criaturas das sombras e coletar fragmentos de conhecimento ancestral.', 15),

-- Tho Mek's Quest (Special NPC from Nebulous Coast)
(2, 'Tho Mek, a luminar da Igreja da Luz, convoca aventureiros para uma missão sagrada. Uma antiga profecia fala sobre uma luz divina que está se apagando nas profundezas da Costa Nebulosa. A missão requer pureza de coração e coragem para enfrentar as sombras que ameaçam extinguir a luz sagrada. Os escolhidos devem coletar cristais luminosos e realizar rituais antigos para reacender a chama divina.', 20),

-- Regular NPC Quests
(3, 'O velho pescador da vila precisa de ajuda para encontrar seu barco perdido durante uma tempestade. A embarcação carrega um amuleto de família que é essencial para proteger a vila de criaturas marinhas. A missão envolve navegar pelas águas traiçoeiras e enfrentar sereias enganadoras.', 5),

(4, 'A curandeira da vila está preocupada com uma doença misteriosa que está afetando as crianças. Ela precisa de ingredientes raros para criar uma poção curativa. A missão leva os aventureiros através de florestas encantadas e pântanos perigosos em busca de ervas medicinais.', 8),

(5, 'O ferreiro local descobriu um novo tipo de minério que pode revolucionar sua arte. Ele precisa de ajuda para estabelecer uma mina segura e proteger os trabalhadores de criaturas subterrâneas. A missão envolve explorar cavernas profundas e negociar com anões mineradores.', 10),

(6, 'O guarda da cidade está investigando uma série de roubos misteriosos. Ele suspeita que um grupo de ladrões está usando magia para cometer os crimes. A missão requer astúcia e habilidade para rastrear os ladrões e recuperar os tesouros roubados.', 12),

(7, 'A bibliotecária da cidade encontrou referências a um livro perdido que contém conhecimentos proibidos. Ela precisa de ajuda para recuperar o livro antes que caia nas mãos erradas. A missão leva os aventureiros através de bibliotecas antigas e catacumbas secretas.', 14),

(8, 'O mestre alquimista está desenvolvendo uma nova poção que pode curar qualquer mal. Ele precisa de ingredientes raros e perigosos de obter. A missão envolve coletar venenos de criaturas mortais e plantas exóticas de locais perigosos.', 16),

(9, 'O líder dos mercadores está preocupado com o aumento de ataques nas rotas comerciais. Ele precisa de guarda-costas para proteger as caravanas e investigar a origem dos ataques. A missão requer força e diplomacia para lidar com bandidos e negociar com tribos nômades.', 18),

(10, 'A arquimaga da cidade está realizando um ritual para fortalecer as barreiras mágicas que protegem a cidade. Ela precisa de ajuda para coletar energia mágica pura de diferentes fontes elementais. A missão leva os aventureiros através de planos elementais e requer conhecimento arcano.', 25);

-- Insert quest instances for characters
INSERT INTO INSTANCIA_QUEST (id_quest, id_personagem, quest_status) VALUES
-- Personagem 1 (Aventureiro iniciante)
(3, 1, FALSE),  -- Quest do pescador (não iniciada)
(4, 1, TRUE),   -- Quest da curandeira (completa)

-- Personagem 2 (Guerreiro experiente)
(1, 2, TRUE),   -- Quest do Orynth (completa)
(5, 2, FALSE),  -- Quest do ferreiro (não iniciada)
(9, 2, TRUE),   -- Quest do líder dos mercadores (completa)

-- Personagem 3 (Mago iniciante)
(4, 3, FALSE),  -- Quest da curandeira (não iniciada)
(7, 3, TRUE),   -- Quest da bibliotecária (completa)

-- Personagem 4 (Clérigo de alto nível)
(2, 4, TRUE),   -- Quest do Tho Mek (completa)
(8, 4, FALSE),  -- Quest do alquimista (não iniciada)
(10, 4, TRUE),  -- Quest da arquimaga (completa)

-- Personagem 5 (Ladino)
(6, 5, TRUE),   -- Quest do guarda (completa)
(9, 5, FALSE);  -- Quest do líder dos mercadores (não iniciada) 