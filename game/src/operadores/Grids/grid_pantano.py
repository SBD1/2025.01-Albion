import pygame
import os
import random
from game.src.ascii_art import grids
from game.src.operadores.Personagem.sprite_personagem import desenhar_personagem_sprite

CELL_SIZE = 32
SPRITE_PATH = os.path.join(os.path.dirname(__file__), '../../../assets/base_out_atlas.png')
SPRITE_PATH_TERRAIN_ATLAS = os.path.join(os.path.dirname(__file__), '../../../assets/terrain_atlas.png')
SPRITE_PATH_MONSTER = os.path.join(os.path.dirname(__file__), '../../../assets/monster.png')

CHAO_PANTANO_RECT = pygame.Rect(416, 160, 30, 30)
BLOCANTE1_PANTANO_RECT = pygame.Rect(192, 735, 222-192,761-735 )
BLOCANTE2_PANTANO_RECT = pygame.Rect(383, 896, 414-383, 925-896)
BLOCANTE3_PANTANO_RECT = pygame.Rect(833, 993, 861-833, 1022-993)
BLOCANTE4_PANTANO_RECT = pygame.Rect(193, 963, 222-193,992-963 )
MONSTER_RECT = pygame.Rect(54, 53, 217-54, 160-53)  # Coordenadas do monstro

COLOR_PLAYER = (0, 255, 0)
COLOR_MONSTER = (255, 0, 0)
COLOR_BLOCK = (100, 100, 100)

def carregar_sprite_chao_pantano():
    sprite_sheet = pygame.image.load(SPRITE_PATH_TERRAIN_ATLAS).convert_alpha()
    chao_p = pygame.Surface((CHAO_PANTANO_RECT.width, CHAO_PANTANO_RECT.height), pygame.SRCALPHA)
    chao_p.blit(sprite_sheet, (0, 0), CHAO_PANTANO_RECT)
    return pygame.transform.scale(chao_p, (CELL_SIZE, CELL_SIZE))


def carregar_sprite_blocante1_pantano():
    sprite_sheet = pygame.image.load(SPRITE_PATH_TERRAIN_ATLAS).convert_alpha()
    blocante1 = pygame.Surface((BLOCANTE1_PANTANO_RECT.width, BLOCANTE1_PANTANO_RECT.height), pygame.SRCALPHA)
    blocante1.blit(sprite_sheet, (0, 0), BLOCANTE1_PANTANO_RECT)
    return pygame.transform.scale(blocante1, (CELL_SIZE, CELL_SIZE))


def carregar_sprite_blocante2_pantano():
    sprite_sheet = pygame.image.load(SPRITE_PATH_TERRAIN_ATLAS).convert_alpha()
    blocante2 = pygame.Surface((BLOCANTE2_PANTANO_RECT.width, BLOCANTE2_PANTANO_RECT.height), pygame.SRCALPHA)
    blocante2.blit(sprite_sheet, (0, 0), BLOCANTE2_PANTANO_RECT)
    return pygame.transform.scale(blocante2, (CELL_SIZE, CELL_SIZE))


def carregar_sprite_blocante3_pantano():
    sprite_sheet = pygame.image.load(SPRITE_PATH_TERRAIN_ATLAS).convert_alpha()
    blocante3 = pygame.Surface((BLOCANTE3_PANTANO_RECT.width, BLOCANTE3_PANTANO_RECT.height), pygame.SRCALPHA)
    blocante3.blit(sprite_sheet, (0, 0), BLOCANTE3_PANTANO_RECT)
    return pygame.transform.scale(blocante3, (CELL_SIZE, CELL_SIZE))


def carregar_sprite_blocante4_pantano():
    sprite_sheet = pygame.image.load(SPRITE_PATH_TERRAIN_ATLAS).convert_alpha()
    blocante4 = pygame.Surface((BLOCANTE4_PANTANO_RECT.width, BLOCANTE4_PANTANO_RECT.height), pygame.SRCALPHA)
    blocante4.blit(sprite_sheet, (0, 0), BLOCANTE4_PANTANO_RECT)
    return pygame.transform.scale(blocante4, (CELL_SIZE, CELL_SIZE))

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


blocante_cache = {}  # Cache para blocantes aleatórios

def desenhar_grid_pantano(screen, grid, pos_jogador, sprite_chao_p, sprite_blocantes, sprite_monstro=None, monstros_sala=None):
    if monstros_sala is None:
        monstros_sala = []
    altura = len(grid)
    largura = len(grid[0])
    # 1. Desenha o chão em todas as células
    for i in range(altura):
        for j in range(largura):
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            for tile_x in range(0, CELL_SIZE, sprite_chao_p.get_width()):
                for tile_y in range(0, CELL_SIZE, sprite_chao_p.get_height()):
                    screen.blit(sprite_chao_p, (x + tile_x, y + tile_y))
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

    # 4. Desenha o jogador
    xj, yj = pos_jogador[1] * CELL_SIZE, pos_jogador[0] * CELL_SIZE
    pygame.draw.rect(screen, COLOR_PLAYER, (xj, yj, CELL_SIZE, CELL_SIZE), 3)


def main_grid_pygame_pantano(nome_sala="Pântano Sombrio", sprites_personagem=None, direcao_atual="baixo"):
    pygame.init()
    grid_data = grids[nome_sala]
    if isinstance(grid_data, list) and isinstance(grid_data[0], str):
        grid = [list(l) for l in grid_data]
        monstros_sala = []
    else:
        grid, monstros_sala = grid_data
        # Limpar apenas emojis de monstros do grid, preservando blocantes
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == "🦠":  # Remove apenas o emoji do monstro do pântano
                    grid[i][j] = " "
    altura, largura = len(grid), len(grid[0])
    screen = pygame.display.set_mode((largura * CELL_SIZE, altura * CELL_SIZE + 40))
    pygame.display.set_caption("Albion Grid Pântano - Pygame")
    sprite_chao_p = carregar_sprite_chao_pantano()
    sprite_blocantes = [
        carregar_sprite_blocante1_pantano(),
        carregar_sprite_blocante2_pantano(),
        carregar_sprite_blocante3_pantano(),
        carregar_sprite_blocante4_pantano()
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
                return "voltar", None
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    return "voltar", None
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
                        return "mudar_sala", direcao
                    if grid[nova_pos[0]][nova_pos[1]] in (" ", "@"):
                        pos_jogador[:] = nova_pos
        screen.fill((0, 0, 0))
        desenhar_grid_pantano(screen, grid, pos_jogador, sprite_chao_p, sprite_blocantes, sprite_monstro, monstros_sala)
        mensagem = "Pressione 'q' para voltar ao menu de ação"
        text = font.render(mensagem, True, (255, 255, 0))
        screen.blit(text, ((screen.get_width() - text.get_width()) // 2, altura * CELL_SIZE + 5))
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    return "voltar", None