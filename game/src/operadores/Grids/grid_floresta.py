import pygame
import os
import random
from game.src.ascii_art import grids
from game.src.operadores.Personagem.sprite_personagem import desenhar_personagem_sprite

CELL_SIZE = 32
SPRITE_PATH = os.path.join(os.path.dirname(__file__), '../../../assets/base_out_atlas.png')
SPRITE_PATH_TERRAIN_ATLAS = os.path.join(os.path.dirname(__file__), '../../../assets/terrain_atlas.png')
SPRITE_PATH_MONSTER = os.path.join(os.path.dirname(__file__), '../../../assets/monster.png')

CHAO_FLORESTA_RECT = pygame.Rect(691, 84, 60, 56)
BLOCANTE1_FLORESTA_RECT = pygame.Rect(774, 484, 76, 91)
BLOCANTE2_FLORESTA_RECT = pygame.Rect(770, 383, 94, 80)
BLOCANTE3_FLORESTA_RECT = pygame.Rect(416, 924, 32, 33)
BLOCANTE4_FLORESTA_RECT = pygame.Rect(481, 896, 28, 62)
MONSTER_RECT = pygame.Rect(54, 53, 217-54, 160-53)  # Coordenadas do monstro

COLOR_PLAYER = (0, 255, 0)
COLOR_MONSTER = (255, 0, 0)
COLOR_BLOCK = (100, 100, 100)

def carregar_sprite_chao_floresta():
    sprite_sheet = pygame.image.load(SPRITE_PATH).convert_alpha()
    chao_f = pygame.Surface((CHAO_FLORESTA_RECT.width, CHAO_FLORESTA_RECT.height), pygame.SRCALPHA)
    chao_f.blit(sprite_sheet, (0, 0), CHAO_FLORESTA_RECT)
    return pygame.transform.scale(chao_f, (CELL_SIZE, CELL_SIZE))


def carregar_sprite_blocante1_floresta():
    sprite_sheet = pygame.image.load(SPRITE_PATH).convert_alpha()
    blocante_f = pygame.Surface((BLOCANTE1_FLORESTA_RECT.width, BLOCANTE1_FLORESTA_RECT.height), pygame.SRCALPHA)
    blocante_f.blit(sprite_sheet, (0, 0), BLOCANTE1_FLORESTA_RECT)
    return pygame.transform.scale(blocante_f, (CELL_SIZE, CELL_SIZE))


def carregar_sprite_blocante2_floresta():
    sprite_sheet = pygame.image.load(SPRITE_PATH).convert_alpha()
    blocante2_f = pygame.Surface((BLOCANTE2_FLORESTA_RECT.width, BLOCANTE2_FLORESTA_RECT.height), pygame.SRCALPHA)
    blocante2_f.blit(sprite_sheet, (0, 0), BLOCANTE2_FLORESTA_RECT)
    return pygame.transform.scale(blocante2_f, (CELL_SIZE, CELL_SIZE))


def carregar_sprite_blocante3_floresta():
    sprite_sheet = pygame.image.load(SPRITE_PATH_TERRAIN_ATLAS).convert_alpha()
    blocante3_f = pygame.Surface((BLOCANTE3_FLORESTA_RECT.width, BLOCANTE3_FLORESTA_RECT.height), pygame.SRCALPHA)
    blocante3_f.blit(sprite_sheet, (0, 0), BLOCANTE3_FLORESTA_RECT)
    return pygame.transform.scale(blocante3_f, (CELL_SIZE, CELL_SIZE))


def carregar_sprite_blocante4_floresta():
    sprite_sheet = pygame.image.load(SPRITE_PATH_TERRAIN_ATLAS).convert_alpha()
    blocante4_f = pygame.Surface((BLOCANTE4_FLORESTA_RECT.width, BLOCANTE4_FLORESTA_RECT.height), pygame.SRCALPHA)
    blocante4_f.blit(sprite_sheet, (0, 0), BLOCANTE4_FLORESTA_RECT)
    return pygame.transform.scale(blocante4_f, (CELL_SIZE, CELL_SIZE))

def carregar_sprite_monstro():
    sprite_sheet = pygame.image.load(SPRITE_PATH_MONSTER).convert_alpha()
    monstro_f = pygame.Surface((MONSTER_RECT.width, MONSTER_RECT.height), pygame.SRCALPHA)
    monstro_f.blit(sprite_sheet, (0, 0), MONSTER_RECT)
    return pygame.transform.scale(monstro_f, (CELL_SIZE, CELL_SIZE))

def carregar_sprite_monstro_floresta():
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

blocante_cache = {}
def desenhar_grid_floresta(screen, grid, pos_jogador, sprite_chao_f, sprite_blocantes, sprite_monstro=None, monstros_sala=None):
    if monstros_sala is None:
        monstros_sala = []
        
    altura = len(grid)
    largura = len(grid[0])
    # 1. Desenha o chão em todas as células
    for i in range(altura):
        for j in range(largura):
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            for tile_x in range(0, CELL_SIZE, sprite_chao_f.get_width()):
                for tile_y in range(0, CELL_SIZE, sprite_chao_f.get_height()):
                    screen.blit(sprite_chao_f, (x + tile_x, y + tile_y))
    # 2. Desenha blocantes, com blocante1 para os limites e outros blocantes para internos
    for i in range(altura):
        for j in range(largura):
            if grid[i][j] not in (" ", "@"):  # base do blocante
                x = j * CELL_SIZE
                y = i * CELL_SIZE
                if i == 0 or j == 0 or i == altura - 1 or j == largura - 1:  # Limites do mapa
                    sprite_blocante = sprite_blocantes[0]  # Blocante do tipo 1
                else:  # Elementos internos
                    if len(sprite_blocantes) > 1:  # Ensure there are internal blocantes to choose from
                        if (i, j) not in blocante_cache:
                            blocante_cache[(i, j)] = random.choice(sprite_blocantes[1:])
                        sprite_blocante = blocante_cache[(i, j)]
                    else:
                        sprite_blocante = sprite_blocantes[0]  # Fallback to blocante 1 if no others are available
                screen.blit(sprite_blocante, (x, y))
    
    # 3. Desenha os monstros nas posições da sala (apenas se não há blocantes)
    if sprite_monstro:
        for monstro_pos in monstros_sala:
            if len(monstro_pos) >= 2:
                mx, my = monstro_pos[0], monstro_pos[1]
                if 0 <= mx < altura and 0 <= my < largura:
                    # Só desenha se a posição estiver livre (não for blocante)
                    if grid[mx][my] in (" ", "@"):
                        xm, ym = my * CELL_SIZE, mx * CELL_SIZE
                        screen.blit(sprite_monstro, (xm, ym))
    
    # 4. Jogador
    xj, yj = pos_jogador[1] * CELL_SIZE, pos_jogador[0] * CELL_SIZE
    pygame.draw.rect(screen, COLOR_PLAYER, (xj, yj, CELL_SIZE, CELL_SIZE), 3)

def main_grid_pygame_floresta(nome_sala="Floresta do Leste", sprites_personagem=None, direcao_atual="baixo"):
    pygame.init()
    grid_data = grids[nome_sala]
    if isinstance(grid_data, list) and isinstance(grid_data[0], str):
        grid = [list(l) for l in grid_data]
        monstros_sala = []
    else:
        grid, monstros_sala = grid_data
        # Limpar apenas emoji de monstros específicos da floresta do grid
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == "👺":  # Remove apenas o emoji específico do monstro da floresta
                    grid[i][j] = " "
    
    altura, largura = len(grid), len(grid[0])
    screen = pygame.display.set_mode((largura * CELL_SIZE, altura * CELL_SIZE + 40))
    pygame.display.set_caption("Albion Grid Floresta - Pygame")
    sprite_chao_f = carregar_sprite_chao_floresta()
    sprite_blocantes = [
        carregar_sprite_blocante1_floresta(),
        carregar_sprite_blocante2_floresta(),
        carregar_sprite_blocante3_floresta(),
        carregar_sprite_blocante4_floresta()
    ]
    sprite_monstro = carregar_sprite_monstro_floresta()
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
                    # Checa se saiu do grid (mudança de sala)
                    if (nova_pos[0] < 0 or nova_pos[0] >= altura or
                        nova_pos[1] < 0 or nova_pos[1] >= largura):
                        running = False
                        return "mudar_sala", direcao, pos_jogador
                    # Checa se a nova posição é blocante
                    if grid[nova_pos[0]][nova_pos[1]] in (" ", "@"):
                        pos_jogador[:] = nova_pos
                        # Verificar se encontrou monstro
                        if tuple(pos_jogador) in monstros_sala:
                            pygame.quit()
                            return "encontrou_monstro", None, pos_jogador
        screen.fill((0, 0, 0))
        desenhar_grid_floresta(screen, grid, pos_jogador, sprite_chao_f, sprite_blocantes, sprite_monstro, monstros_sala)
        mensagem = "Pressione 'q' para voltar ao menu de ação"
        text = font.render(mensagem, True, (255, 255, 0))
        screen.blit(text, ((screen.get_width() - text.get_width()) // 2, altura * CELL_SIZE + 5))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    return "voltar", None, pos_jogador