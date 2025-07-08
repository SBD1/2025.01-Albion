import pygame
import os
import random
from game.src.ascii_art import grids
from game.src.operadores.Personagem.sprite_personagem import desenhar_personagem_sprite

# Configurações básicas
CELL_SIZE = 32
SPRITE_PATH_TERRAIN_ATLAS = os.path.join(os.path.dirname(__file__), '../../../assets/terrain_atlas.png')
SPRITE_PATH_MONSTER = os.path.join(os.path.dirname(__file__), '../../../assets/monster.png')

# Retângulos para recorte dos sprites
CHAO_RUINAS_RECT = pygame.Rect(607, 704, 640-607, 735-704)  # Chão de ruínas
BLOCANTE1_RUINAS_RECT = pygame.Rect(608, 484, 639-608, 576-484)  # Pilares e paredes
BLOCANTE2_RUINAS_RECT = pygame.Rect(865, 851, 58, 41)  # Escombros
BLOCANTE3_RUINAS_RECT = pygame.Rect(447, 383, 479-447, 479-383)  # Borda da ruína
MONSTER_RECT = pygame.Rect(54, 53, 217-54, 160-53)  # Coordenadas do monstro

# Configurações visuais
COLOR_PLAYER = (255, 0, 0)  # Cor vermelha para o jogador
blocante_cache = {}  # Cache para blocantes aleatórios

def carregar_sprite_chao_ruinas():
    """Carrega o sprite do chão das ruínas."""
    sprite_sheet = pygame.image.load(SPRITE_PATH_TERRAIN_ATLAS).convert_alpha()
    chao_r = pygame.Surface((CHAO_RUINAS_RECT.width, CHAO_RUINAS_RECT.height), pygame.SRCALPHA)
    chao_r.blit(sprite_sheet, (0, 0), CHAO_RUINAS_RECT)
    return pygame.transform.scale(chao_r, (CELL_SIZE, CELL_SIZE))

def carregar_sprite_blocante1_ruinas():
    """Carrega o sprite dos pilares e paredes."""
    sprite_sheet = pygame.image.load(SPRITE_PATH_TERRAIN_ATLAS).convert_alpha()
    blocante1 = pygame.Surface((BLOCANTE1_RUINAS_RECT.width, BLOCANTE1_RUINAS_RECT.height), pygame.SRCALPHA)
    blocante1.blit(sprite_sheet, (0, 0), BLOCANTE1_RUINAS_RECT)
    return pygame.transform.scale(blocante1, (CELL_SIZE, CELL_SIZE))

def carregar_sprite_blocante2_ruinas():
    """Carrega o sprite dos escombros."""
    sprite_sheet = pygame.image.load(SPRITE_PATH_TERRAIN_ATLAS).convert_alpha()
    blocante2 = pygame.Surface((BLOCANTE2_RUINAS_RECT.width, BLOCANTE2_RUINAS_RECT.height), pygame.SRCALPHA)
    blocante2.blit(sprite_sheet, (0, 0), BLOCANTE2_RUINAS_RECT)
    return pygame.transform.scale(blocante2, (CELL_SIZE, CELL_SIZE))

def carregar_sprite_blocante3_ruinas():
    """Carrega o sprite da borda da ruína."""
    sprite_sheet = pygame.image.load(SPRITE_PATH_TERRAIN_ATLAS).convert_alpha()
    blocante3 = pygame.Surface((BLOCANTE3_RUINAS_RECT.width, BLOCANTE3_RUINAS_RECT.height), pygame.SRCALPHA)
    blocante3.blit(sprite_sheet, (0, 0), BLOCANTE3_RUINAS_RECT)
    return pygame.transform.scale(blocante3, (CELL_SIZE, CELL_SIZE))

def carregar_sprite_monstro():
    """Carrega o sprite do monstro usando as coordenadas especificadas."""
    try:
        sprite_sheet = pygame.image.load(SPRITE_PATH_MONSTER).convert_alpha()
        monster_sprite = pygame.Surface((MONSTER_RECT.width, MONSTER_RECT.height), pygame.SRCALPHA)
        monster_sprite.blit(sprite_sheet, (0, 0), MONSTER_RECT)
        return pygame.transform.scale(monster_sprite, (CELL_SIZE, CELL_SIZE))
    except pygame.error as e:
        print(f"Erro ao carregar sprite do monstro: {e}")
        # Retorna um sprite vermelho como fallback
        fallback = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        fallback.fill((255, 0, 0))
        return fallback

def is_posicao_pilar(i, j, altura, largura):
    """Determina se uma posição deve ter um pilar baseado em um padrão simétrico."""
    # Distância das bordas para começar os pilares
    margem = 3
    # Espaçamento entre pilares
    espacamento = 4
    
    # Verifica se está dentro da área válida para pilares
    if margem <= i < altura - margem and margem <= j < largura - margem:
        # Cria padrão simétrico para pilares
        if (i - margem) % espacamento == 0 and (j - margem) % espacamento == 0:
            return True
        # Cria "paredes" parciais conectando alguns pilares
        if ((i - margem) % espacamento == 0 and (j - margem) % 2 == 0) or \
           ((j - margem) % espacamento == 0 and (i - margem) % 2 == 0):
            return random.random() < 0.3  # 30% de chance de ter uma parede
    return False

def desenhar_grid_ruinas(screen, grid, pos_jogador, sprite_chao_r, sprite_blocantes, sprite_monstro, monstros_sala=None):
    """Desenha o grid das ruínas com um padrão estrutural simétrico."""
    if monstros_sala is None:
        monstros_sala = []
        
    altura = len(grid)
    largura = len(grid[0])

    # 1. Desenha o chão em todas as células
    for i in range(altura):
        for j in range(largura):
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            for tile_x in range(0, CELL_SIZE, sprite_chao_r.get_width()):
                for tile_y in range(0, CELL_SIZE, sprite_chao_r.get_height()):
                    screen.blit(sprite_chao_r, (x + tile_x, y + tile_y))

    # 2. Desenha blocantes com padrão de ruínas
    for i in range(altura):
        for j in range(largura):
            if grid[i][j] not in (" ", "@"):
                x = j * CELL_SIZE
                y = i * CELL_SIZE
                
                # Bordas do mapa
                if i == 0 or j == 0 or i == altura - 1 or j == largura - 1:
                    screen.blit(sprite_blocantes[2], (x, y))  # Borda da ruína
                else:
                    # Verifica se a posição já está no cache
                    if (i, j) not in blocante_cache:
                        # Define o tipo de blocante baseado na posição
                        if is_posicao_pilar(i, j, altura, largura):
                            blocante_cache[(i, j)] = sprite_blocantes[0]  # Pilares e paredes
                        else:
                            blocante_cache[(i, j)] = random.choice([sprite_blocantes[1]])  # Escombros
                    
                    screen.blit(blocante_cache[(i, j)], (x, y))

    # 3. Desenha os monstros nas posições da sala (apenas se não há blocantes)
    for monstro_pos in monstros_sala:
        if len(monstro_pos) >= 2:
            mx, my = monstro_pos[0], monstro_pos[1]
            if 0 <= mx < altura and 0 <= my < largura:
                # Só desenha se a posição estiver livre (não for blocante)
                if grid[mx][my] in (" ", "@"):
                    xm, ym = my * CELL_SIZE, mx * CELL_SIZE
                    screen.blit(sprite_monstro, (xm, ym))

    # 4. Desenha o jogador
    xj, yj = pos_jogador[1] * CELL_SIZE, pos_jogador[0] * CELL_SIZE
    pygame.draw.rect(screen, COLOR_PLAYER, (xj, yj, CELL_SIZE, CELL_SIZE), 3)

def verificar_movimento(pos_jogador, direcao, grid, sala_info):
    """Verifica se o movimento é possível e se leva a uma nova sala."""
    altura = len(grid)
    largura = len(grid[0])
    x, y = pos_jogador

    if direcao == "norte" and x == 1 and y == largura // 2 and sala_info['conexao_norte']:
        return True, "norte"
    elif direcao == "sul" and x == altura - 2 and y == largura // 2 and sala_info['conexao_sul']:
        return True, "sul"
    elif direcao == "leste" and x == altura // 2 and y == largura - 2 and sala_info['conexao_leste']:
        return True, "leste"
    elif direcao == "oeste" and x == altura // 2 and y == 1 and sala_info['conexao_oeste']:
        return True, "oeste"

    # Verifica se pode mover dentro da mesma sala
    novo_x, novo_y = x, y
    if direcao == "norte" and x > 0:
        novo_x -= 1
    elif direcao == "sul" and x < altura - 1:
        novo_x += 1
    elif direcao == "oeste" and y > 0:
        novo_y -= 1
    elif direcao == "leste" and y < largura - 1:
        novo_y += 1

    if 0 <= novo_x < altura and 0 <= novo_y < largura and grid[novo_x][novo_y] in (" ", "@"):
        pos_jogador[0], pos_jogador[1] = novo_x, novo_y
        return False, None

    return False, None

def main_grid_pygame_ruinas(nome_sala="Ruínas Antigas", sprites_personagem=None, direcao_atual="baixo"):
    """Função principal para renderizar e controlar o grid das ruínas."""
    pygame.init()
    grid_data = grids[nome_sala]
    if isinstance(grid_data, list) and isinstance(grid_data[0], str):
        grid = [list(l) for l in grid_data]
        monstros_sala = []
    else:
        grid, monstros_sala = grid_data
        # Limpar apenas emoji de monstros específicos das ruínas do grid
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == "🗿":  # Remove apenas o emoji específico do monstro das ruínas
                    grid[i][j] = " "
    
    altura, largura = len(grid), len(grid[0])
    screen = pygame.display.set_mode((largura * CELL_SIZE, altura * CELL_SIZE + 40))
    pygame.display.set_caption("Albion Grid Ruínas - Pygame")
    sprite_chao_r = carregar_sprite_chao_ruinas()
    sprite_blocantes = [
        carregar_sprite_blocante1_ruinas(),
        carregar_sprite_blocante2_ruinas(),
        carregar_sprite_blocante3_ruinas()
    ]
    sprite_monstro = carregar_sprite_monstro()
    pos_jogador = [7, 25] if largura > 25 else [altura//2, largura//2]
    clock = pygame.time.Clock()
    running = True
    font = pygame.font.SysFont(None, 32)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "voltar", None, pos_jogador
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    pygame.quit()
                    return "voltar", None, pos_jogador
                direcao = None
                nova_pos = pos_jogador.copy()
                if event.key == pygame.K_UP:
                    direcao = "norte"
                    nova_pos[0] -= 1
                elif event.key == pygame.K_DOWN:
                    direcao = "sul"
                    nova_pos[0] += 1
                elif event.key == pygame.K_LEFT:
                    direcao = "oeste"
                    nova_pos[1] -= 1
                elif event.key == pygame.K_RIGHT:
                    direcao = "leste"
                    nova_pos[1] += 1
                if direcao:
                    if (nova_pos[0] < 0 or nova_pos[0] >= altura or
                        nova_pos[1] < 0 or nova_pos[1] >= largura):
                        running = False
                        return "mudar_sala", direcao, pos_jogador
                    if grid[nova_pos[0]][nova_pos[1]] in (" ", "@"):
                        pos_jogador[:] = nova_pos
                        # Verificar se encontrou monstro
                        if tuple(pos_jogador) in monstros_sala:
                            pygame.quit()
                            return "encontrou_monstro", None, pos_jogador
        screen.fill((0, 0, 0))
        desenhar_grid_ruinas(screen, grid, pos_jogador, sprite_chao_r, sprite_blocantes, sprite_monstro, monstros_sala)
        mensagem = "Pressione 'q' para voltar ao menu de ação"
        text = font.render(mensagem, True, (255, 255, 0))
        screen.blit(text, ((screen.get_width() - text.get_width()) // 2, altura * CELL_SIZE + 5))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    return "voltar", None, pos_jogador

if __name__ == "__main__":
    # Exemplo de uso com dados fictícios de sala
    sala_teste = {
        'nome': 'Ruínas Antigas',
        'conexao_norte': 1,
        'conexao_sul': None,
        'conexao_leste': 3,
        'conexao_oeste': 2
    }
    main_grid_pygame_ruinas(sala_teste)