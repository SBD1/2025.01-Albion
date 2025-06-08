INSERT INTO public.SALA (id_sala, nome, descricao, conexao_norte, conexao_sul, conexao_leste, conexao_oeste) VALUES

(1, 'Praça Central', 'O coração do reino, onde os jogadores iniciam sua jornada.', 
 2, 3, 4, 5),

(2, 'Campos Congelados', 'Terras geladas e traiçoeiras ao norte da Praça Central.',
 6, 1, 7, NULL),

(3, 'Caverna Sombria', 'Uma caverna úmida e silenciosa, com rumores de monstros ocultos.',
 1, 8, NULL, NULL),

(4, 'Deserto Escaldante', 'Dunas sem fim e calor intenso ao leste da Praça Central.',
 NULL, 8, NULL, 1),

(5, 'Pântano Sombrio', 'Área pantanosa e misteriosa, cheia de criaturas hostis.',
 NULL, NULL, 1, NULL),

(6, 'Montanha Nevada', 'Topo nevado e ventos congelantes, lar de bestas ferozes.',
 NULL, 2, NULL, NULL),

(7, 'Floresta do Leste', 'Floresta viva e encantada com armadilhas naturais.',
 NULL, NULL, NULL, 2),

(8, 'Ruínas Antigas', 'Antiga civilização caída, agora lar de espíritos inquietos.',
 3, NULL, NULL, 4),

(9, 'Cânion Vermelho', 'Fendas profundas e caminhos traiçoeiros entre as pedras.', 
 NULL, NULL, NULL, NULL),

(10, 'Costa Nebulosa', 'Litoral envolto em neblina, onde o mar e o desconhecido se encontram.',
 NULL, NULL, NULL, NULL);
