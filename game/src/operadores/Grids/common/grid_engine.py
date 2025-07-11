import pygame
from ascii_art import grids
from .sprite_loader import SpriteLoader
from .grid_renderer import GridRenderer

class GridEngine:
    def __init__(self, biome_config):
        self.config = biome_config
        self.sprites = {}
        self.blocante_cache = {}
        self.CELL_SIZE = 58
        
    def load_sprites(self):
        """Carrega todos os sprites necessários para o bioma."""
        self.sprites = SpriteLoader.load_biome_sprites(self.config)
    
    def setup_grid_data(self, nome_sala):
        
        grid_data = grids[nome_sala]
        
        if isinstance(grid_data, list) and isinstance(grid_data[0], str):
            grid = [list(l) for l in grid_data]
            monstros_sala = []
        else:
            grid, monstros_sala = grid_data
            
            if 'monster_emoji' in self.config:
                emoji = self.config['monster_emoji']
                for i in range(len(grid)):
                    for j in range(len(grid[0])):
                        if grid[i][j] == emoji:
                            grid[i][j] = " "
        
        return grid, monstros_sala
    
    def handle_movement(self, event, pos_jogador, grid, direcao_atual):
        """
        Processa eventos de movimento mantendo a lógica original.
        
        Args:
            event: Evento do pygame
            pos_jogador (list): Posição atual do jogador
            grid (list): Grid do mapa
            direcao_atual (str): Direção atual do personagem
            
        Returns:
            tuple: (resultado, direcao_movimento, nova_pos, nova_direcao)
        """
        if event.type == pygame.QUIT:
            return "voltar", None, pos_jogador, direcao_atual
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                return "voltar", None, pos_jogador, direcao_atual
            
            # Mapeia teclas para direções
            direcao_map = {
                pygame.K_UP: "norte",
                pygame.K_DOWN: "sul", 
                pygame.K_LEFT: "oeste",
                pygame.K_RIGHT: "leste"
            }
            
            if event.key in direcao_map:
                direcao = direcao_map[event.key]
                nova_pos = pos_jogador.copy()
                
                # Atualiza posição baseada na direção
                if direcao == "norte":
                    nova_pos[0] -= 1
                elif direcao == "sul":
                    nova_pos[0] += 1
                elif direcao == "oeste":
                    nova_pos[1] -= 1
                elif direcao == "leste":
                    nova_pos[1] += 1
                
                altura = len(grid)
                largura = len(grid[0])
                
                # Verifica se saiu do grid (mudança de sala)
                if (nova_pos[0] < 0 or nova_pos[0] >= altura or
                    nova_pos[1] < 0 or nova_pos[1] >= largura):
                    return "mudar_sala", direcao, pos_jogador, direcao_atual
                
                # Verifica se a nova posição não é blocante
                if grid[nova_pos[0]][nova_pos[1]] in (" ", "@"):
                    return "movimento_valido", None, nova_pos, direcao
        
        return None, None, pos_jogador, direcao_atual
    
    def check_monster_encounter(self, pos_jogador, monstros_sala):
        """
        Verifica se o jogador encontrou um monstro.
        
        Args:
            pos_jogador (list): Posição do jogador
            monstros_sala (list): Lista de posições dos monstros
            
        Returns:
            bool: True se encontrou monstro
        """
        return tuple(pos_jogador) in monstros_sala
    
    def render_grid(self, screen, grid, pos_jogador, monstros_sala, sprites_personagem=None, direcao_atual="baixo"):
        """
        Renderiza o grid completo.
        
        Args:
            screen (pygame.Surface): Superfície de desenho
            grid (list): Grid do mapa
            pos_jogador (list): Posição do jogador
            monstros_sala (list): Lista de posições dos monstros
            sprites_personagem (dict): Sprites do personagem
            direcao_atual (str): Direção atual do personagem
        """
        # Calcular offset para centralizar o grid na tela
        altura, largura = len(grid), len(grid[0])
        screen_width, screen_height = screen.get_size()
        grid_width = largura * self.CELL_SIZE
        grid_height = altura * self.CELL_SIZE
        
        offset_x = max(0, (screen_width - grid_width) // 2)
        offset_y = max(0, (screen_height - grid_height) // 2)
        offset = (offset_x, offset_y)
        
        # Preenche fundo preto
        screen.fill((0, 0, 0))
        
        # Renderiza chão
        GridRenderer.renderizar_chao(screen, grid, self.sprites['chao'], self.CELL_SIZE, offset)
        
        # Renderiza blocantes
        GridRenderer.renderizar_blocantes(screen, grid, self.sprites['blocantes'], self.CELL_SIZE, offset, self.blocante_cache)
        
        # Renderiza monstros
        if 'monster' in self.sprites:
            GridRenderer.renderizar_monstro(screen, grid, monstros_sala, self.sprites['monster'], self.CELL_SIZE, offset)
        
        # Renderiza jogador
        player_color = self.config.get('colors', {}).get('player', (255, 255, 255))
        GridRenderer.renderizar_personagem(screen, pos_jogador, player_color, self.CELL_SIZE, offset, sprites_personagem, direcao_atual)
        
        # Renderiza UI
        font = pygame.font.SysFont(None, 32)
        GridRenderer.render_ui(screen, grid, font)
    
    def run_grid(self, nome_sala, sprites_personagem=None, direcao_atual="baixo", screen=None):
        """
        Executa o loop principal do grid.
        
        Args:
            nome_sala (str): Nome da sala
            sprites_personagem (dict): Sprites do personagem
            direcao_atual (str): Direção inicial do personagem
            screen (pygame.Surface): Tela existente (opcional, cria nova se None)
            
        Returns:
            tuple: (resultado, direcao_movimento, pos_final, direcao_final)
        """
        
        # Inicialização completa do pygame
        pygame.init()
        pygame.font.init()
        
        # Carrega sprites
        self.load_sprites()
        
        # Prepara dados do grid
        grid, monstros_sala = self.setup_grid_data(nome_sala)
        
        # Usa tela existente ou cria nova janela em tela cheia
        if screen is None:
            info = pygame.display.Info()
            screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.FULLSCREEN)
            pygame.display.set_caption(f"Albion Grid {self.config['nome']} - Pygame")
        
        # Posição inicial do jogador
        altura, largura = len(grid), len(grid[0])
        pos_jogador = [7, 16] if largura > 16 else [altura//2, largura//2]
        
        # Loop principal
        clock = pygame.time.Clock()
        running = True
        font = pygame.font.SysFont(None, 32)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return "voltar", None, pos_jogador, direcao_atual
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        return "voltar", None, pos_jogador, direcao_atual
                    
                    # Processa movimento
                    direcao_movimento = None
                    nova_pos = pos_jogador.copy()
                    nova_direcao = direcao_atual
                    
                    if event.key == pygame.K_UP:
                        direcao_movimento = "norte"
                        nova_pos[0] -= 1
                        nova_direcao = "cima"
                    elif event.key == pygame.K_DOWN:
                        direcao_movimento = "sul"
                        nova_pos[0] += 1
                        nova_direcao = "baixo"
                    elif event.key == pygame.K_LEFT:
                        direcao_movimento = "oeste"
                        nova_pos[1] -= 1
                        nova_direcao = "esquerda"
                    elif event.key == pygame.K_RIGHT:
                        direcao_movimento = "leste"
                        nova_pos[1] += 1
                        nova_direcao = "direita"
                    
                    if direcao_movimento:
                        # Atualiza a direção do personagem independentemente do movimento
                        direcao_atual = nova_direcao
                        
                        # Verifica se saiu dos limites da tela (mudança de sala)
                        if (nova_pos[0] < 0 or nova_pos[0] >= altura or
                            nova_pos[1] < 0 or nova_pos[1] >= largura):
                            running = False
                            return "mudar_sala", direcao_movimento, pos_jogador, direcao_atual
                        
                        # Verifica se pode se mover para a nova posição
                        if grid[nova_pos[0]][nova_pos[1]] in (" ", "@"):
                            pos_jogador[:] = nova_pos
                            
                            # Verifica se encontrou um monstro
                            if tuple(pos_jogador) in monstros_sala:
                                return "encontrou_monstro", None, pos_jogador, direcao_atual
            
            # Renderiza tudo
            screen.fill((0, 0, 0))
            self.render_grid(screen, grid, pos_jogador, monstros_sala, sprites_personagem, direcao_atual)
            
            # Desenha texto de instrução
            mensagem = "Pressione 'q' para voltar ao menu de ação"
            text = font.render(mensagem, True, (255, 255, 0))
            screen.blit(text, ((screen.get_width() - text.get_width()) // 2, altura * self.CELL_SIZE + 5))
            
            pygame.display.flip()
            clock.tick(30)
        
        return "voltar", None, pos_jogador, direcao_atual
