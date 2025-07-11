import pygame
import random

class GridRenderer:
    CELL_SIZE = 58
    
    @staticmethod
    def renderizar_chao(screen, grid, ground_sprite, cell_size=None, offset=None):
        """
        Renderiza o chão do grid.
        
        Args:
            screen (pygame.Surface): Superfície de desenho
            grid (list): Grid do mapa
            ground_sprite (pygame.Surface): Sprite do chão
            cell_size (int): Tamanho da célula (opcional)
            offset (tuple): Offset de posição (opcional)
        """
        if cell_size is None:
            cell_size = GridRenderer.CELL_SIZE
        if offset is None:
            offset = (0, 0)
            
        offset_x, offset_y = offset
        altura = len(grid)
        largura = len(grid[0])
        
        for i in range(altura):
            for j in range(largura):
                x = offset_x + j * cell_size
                y = offset_y + i * cell_size
                
                # Renderiza o chão em ladrilhos para cobrir toda a célula
                for tile_x in range(0, cell_size, ground_sprite.get_width()):
                    for tile_y in range(0, cell_size, ground_sprite.get_height()):
                        screen.blit(ground_sprite, (x + tile_x, y + tile_y))
    
    @staticmethod
    def renderizar_blocantes(screen, grid, blocker_sprites, cell_size=None, offset=None, blocante_cache=None):
        """
        Renderiza os blocantes do grid mantendo a lógica original.
        
        Args:
            screen (pygame.Surface): Superfície de desenho
            grid (list): Grid do mapa
            blocker_sprites (list): Lista de sprites dos blocantes
            cell_size (int): Tamanho da célula (opcional)
            offset (tuple): Offset de posição (opcional)
            blocante_cache (dict): Cache para persistência dos blocantes aleatórios
        """
        if cell_size is None:
            cell_size = GridRenderer.CELL_SIZE
        if offset is None:
            offset = (0, 0)
        if blocante_cache is None:
            blocante_cache = {}
            
        offset_x, offset_y = offset
        altura = len(grid)
        largura = len(grid[0])
        
        for i in range(altura):
            for j in range(largura):
                if grid[i][j] not in (" ", "@"):  # Posição tem blocante
                    x = offset_x + j * cell_size
                    y = offset_y + i * cell_size
                    
                    # Lógica original: blocante1 para limites, outros para internos
                    if i == 0 or j == 0 or i == altura - 1 or j == largura - 1:
                        # Limites do mapa - sempre blocante tipo 1
                        sprite_blocante = blocker_sprites[0]
                    else:
                        # Elementos internos - escolha aleatória persistente
                        if len(blocker_sprites) > 1:
                            if (i, j) not in blocante_cache:
                                blocante_cache[(i, j)] = random.choice(blocker_sprites[1:])
                            sprite_blocante = blocante_cache[(i, j)]
                        else:
                            sprite_blocante = blocker_sprites[0]  # Fallback
                    
                    # Redimensionar sprite se necessário
                    if sprite_blocante.get_size() != (cell_size, cell_size):
                        sprite_blocante = pygame.transform.scale(sprite_blocante, (cell_size, cell_size))
                    
                    screen.blit(sprite_blocante, (x, y))
    
    @staticmethod
    def renderizar_monstro(screen, grid, monstros_sala, monster_sprite, cell_size=None, offset=None):
        """
        Renderiza os monstros nas posições da sala.
        
        Args:
            screen (pygame.Surface): Superfície de desenho
            grid (list): Grid do mapa
            monstros_sala (list): Lista de posições dos monstros
            monster_sprite (pygame.Surface): Sprite do monstro
            cell_size (int): Tamanho da célula (opcional)
            offset (tuple): Offset de posição (opcional)
        """
        if not monster_sprite or not monstros_sala:
            return
        if cell_size is None:
            cell_size = GridRenderer.CELL_SIZE
        if offset is None:
            offset = (0, 0)
            
        offset_x, offset_y = offset
        altura = len(grid)
        largura = len(grid[0])
        
        for monstro_pos in monstros_sala:
            if len(monstro_pos) >= 2:
                mx, my = monstro_pos[0], monstro_pos[1]
                
                # Verifica se a posição é válida
                if 0 <= mx < altura and 0 <= my < largura:
                    # Só desenha se a posição estiver livre (não for blocante)
                    if grid[mx][my] in (" ", "@"):
                        xm = offset_x + my * cell_size
                        ym = offset_y + mx * cell_size
                        
                        # Redimensionar sprite se necessário
                        if monster_sprite.get_size() != (cell_size, cell_size):
                            monster_sprite = pygame.transform.scale(monster_sprite, (cell_size, cell_size))
                        
                        screen.blit(monster_sprite, (xm, ym))
    
    @staticmethod
    def renderizar_personagem(screen, pos_jogador, player_color, cell_size=None, offset=None, sprites_personagem=None, direcao_atual="baixo"):
        """
        Renderiza o jogador usando sprites ou cor de fallback.
        
        Args:
            screen (pygame.Surface): Superfície de desenho
            pos_jogador (list): Posição do jogador [x, y]
            player_color (tuple): Cor do jogador para fallback
            cell_size (int): Tamanho da célula (opcional, usa CELL_SIZE se None)
            offset (tuple): Offset de posição (opcional, usa (0,0) se None)
            sprites_personagem (dict): Sprites do personagem (opcional)
            direcao_atual (str): Direção atual do personagem
        """
        if cell_size is None:
            cell_size = GridRenderer.CELL_SIZE
        if offset is None:
            offset = (0, 0)
            
        offset_x, offset_y = offset
        
        if sprites_personagem:
            # Usa a função original para desenhar sprites do personagem
            # Ajustando para o novo offset
            from operadores.Personagem.sprite_personagem import desenhar_personagem_sprite
            # Temporariamente ajustar a posição para incluir o offset
            pos_adjusted = [pos_jogador[0], pos_jogador[1]]
            # A função desenhar_personagem_sprite será atualizada separadamente
            desenhar_personagem_sprite(screen, pos_adjusted, direcao_atual, sprites_personagem, cell_size, offset)
        else:
            # Fallback para retângulo colorido
            xj = offset_x + pos_jogador[1] * cell_size
            yj = offset_y + pos_jogador[0] * cell_size
            pygame.draw.rect(screen, player_color, (xj, yj, cell_size, cell_size), 3)
    
    @staticmethod
    def render_ui(screen, grid, font, message="Pressione 'q' para voltar ao menu de ação"):
        """
        Renderiza a interface do usuário (mensagem na parte inferior).
        
        Args:
            screen (pygame.Surface): Superfície de desenho
            grid (list): Grid do mapa (para calcular posição)
            font (pygame.font.Font): Fonte para o texto
            message (str): Mensagem a ser exibida
        """
        altura = len(grid)
        text = font.render(message, True, (255, 255, 0))
        text_x = (screen.get_width() - text.get_width()) // 2
        text_y = altura * GridRenderer.CELL_SIZE + 5
        screen.blit(text, (text_x, text_y))
