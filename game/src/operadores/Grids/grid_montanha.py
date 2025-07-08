import pygame
import os
import random
from game.src.ascii_art import grids
from game.src.operadores.Personagem.sprite_personagem import desenhar_personagem_sprite

# Configurações básicas
CELL_SIZE = 32
SPRITE_PATH = os.path.join(os.path.dirname(__file__), '../../../assets/image.png')
SPRITE_PATH_TERRAIN_ATLAS = os.path.join(os.path.dirname(__file__), '../../../assets/terrain_atlas.png')
SPRITE_PATH_MONSTER = os.path.join(os.path.dirname(__file__), '../../../assets/monster.png')

# Retângulos para recorte dos sprites
CHAO_MONTANHA_RECT = pygame.Rect(250, 580, 50, 638-580)  # Chão rochoso
BLOCANTE1_MONTANHA_RECT = pygame.Rect(0, 515, 120, 640-515)  # Parede de pedra
BLOCANTE2_MONTANHA_RECT = pygame.Rect(0, 515, 120, 640-515) # Rocha grande
BLOCANTE3_MONTANHA_RECT = pygame.Rect(317, 0, 457-317, 63)  # Pico nevado
BLOCANTE4_MONTANHA_RECT = pygame.Rect(317, 0, 457-317, 63)  # Cristais
MONSTER_RECT = pygame.Rect(54, 53, 217-54, 160-53)  # Coordenadas do monstro

# Cache global para persistência dos blocantes
blocante_cache = {}

# Cores
COLOR_PLAYER = (139, 69, 19)  # Marrom para o jogador na montanha
COLOR_MONSTER = (255, 0, 0)
COLOR_BLOCK = (100, 100, 100)

def carregar_sprite_chao_montanha():
    """Carrega e redimensiona o sprite do chão rochoso."""
    sprite_sheet = pygame.image.load(SPRITE_PATH).convert_alpha()
    chao = pygame.Surface((CHAO_MONTANHA_RECT.width, CHAO_MONTANHA_RECT.height), pygame.SRCALPHA)
    chao.blit(sprite_sheet, (0, 0), CHAO_MONTANHA_RECT)
    return pygame.transform.scale(chao, (CELL_SIZE, CELL_SIZE))

def carregar_sprite_blocante1_montanha():
    """Carrega e redimensiona o sprite da parede de pedra."""
    sprite_sheet = pygame.image.load(SPRITE_PATH).convert_alpha()
    blocante = pygame.Surface((BLOCANTE1_MONTANHA_RECT.width, BLOCANTE1_MONTANHA_RECT.height), pygame.SRCALPHA)
    blocante.blit(sprite_sheet, (0, 0), BLOCANTE1_MONTANHA_RECT)
    return pygame.transform.scale(blocante, (CELL_SIZE, CELL_SIZE))

def carregar_sprite_blocante2_montanha():
    """Carrega e redimensiona o sprite da rocha grande."""
    sprite_sheet = pygame.image.load(SPRITE_PATH).convert_alpha()
    blocante = pygame.Surface((BLOCANTE2_MONTANHA_RECT.width, BLOCANTE2_MONTANHA_RECT.height), pygame.SRCALPHA)
    blocante.blit(sprite_sheet, (0, 0), BLOCANTE2_MONTANHA_RECT)
    return pygame.transform.scale(blocante, (CELL_SIZE, CELL_SIZE))

def carregar_sprite_blocante3_montanha():
    """Carrega e redimensiona o sprite do pico nevado."""
    sprite_sheet = pygame.image.load(SPRITE_PATH).convert_alpha()
    blocante = pygame.Surface((BLOCANTE3_MONTANHA_RECT.width, BLOCANTE3_MONTANHA_RECT.height), pygame.SRCALPHA)
    blocante.blit(sprite_sheet, (0, 0), BLOCANTE3_MONTANHA_RECT)
    return pygame.transform.scale(blocante, (CELL_SIZE, CELL_SIZE))

def carregar_sprite_blocante4_montanha():
    """Carrega e redimensiona o sprite dos cristais."""
    sprite_sheet = pygame.image.load(SPRITE_PATH).convert_alpha()
    blocante = pygame.Surface((BLOCANTE4_MONTANHA_RECT.width, BLOCANTE4_MONTANHA_RECT.height), pygame.SRCALPHA)
    blocante.blit(sprite_sheet, (0, 0), BLOCANTE4_MONTANHA_RECT)
    return pygame.transform.scale(blocante, (CELL_SIZE, CELL_SIZE))

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

def desenhar_grid_montanha(screen, grid, pos_jogador, sprite_chao, sprite_blocantes, sprite_monstro=None, monstros_sala=None, sprites_personagem=None, direcao_atual="baixo"):
    """Desenha o grid da montanha com chão, blocantes e jogador."""
    if monstros_sala is None:
        monstros_sala = []
    altura = len(grid)
    largura = len(grid[0])

    # 1. Desenha o chão em todas as células
    for i in range(altura):
        for j in range(largura):
            x = j * CELL_SIZE
            y = i * CELL_SIZE
            for tile_x in range(0, CELL_SIZE, sprite_chao.get_width()):
                for tile_y in range(0, CELL_SIZE, sprite_chao.get_height()):
                    screen.blit(sprite_chao, (x + tile_x, y + tile_y))

    # 2. Desenha blocantes
    for i in range(altura):
        for j in range(largura):
            if grid[i][j] not in (" ", "@"):
                x = j * CELL_SIZE
                y = i * CELL_SIZE
                if i == 0 or j == 0 or i == altura - 1 or j == largura - 1:
                    sprite_blocante = sprite_blocantes[0]  # Parede de pedra
                else:
                    if len(sprite_blocantes) > 1:
                        if (i, j) not in blocante_cache:
                            blocante_cache[(i, j)] = random.choice(sprite_blocantes[1:])
                        sprite_blocante = blocante_cache[(i, j)]
                    else:
                        sprite_blocante = sprite_blocantes[0]
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
    if sprites_personagem:
        desenhar_personagem_sprite(screen, pos_jogador, direcao_atual, sprites_personagem)
    else:
        # Fallback para desenho com retângulo se sprites não estiverem disponíveis
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

def main_grid_pygame_montanha(nome_sala="Montanha Nevada", sprites_personagem=None, direcao_atual="baixo"):
    pygame.init()
    grid_data = grids[nome_sala]
    if isinstance(grid_data, list) and isinstance(grid_data[0], str):
        grid = [list(l) for l in grid_data]
        monstros_sala = []
    else:
        grid, monstros_sala = grid_data
        # Limpar apenas emoji de monstros específicos da montanha do grid
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j] == "🧌":  # Remove apenas o emoji específico do monstro da montanha
                    grid[i][j] = " "
    altura, largura = len(grid), len(grid[0])
    screen = pygame.display.set_mode((largura * CELL_SIZE, altura * CELL_SIZE + 40))
    pygame.display.set_caption("Albion Grid Montanha Nevada - Pygame")
    sprite_chao = carregar_sprite_chao_montanha()
    sprite_blocantes = [
        carregar_sprite_blocante1_montanha(),
        carregar_sprite_blocante2_montanha(),
        carregar_sprite_blocante3_montanha(),
        carregar_sprite_blocante4_montanha()
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
                return "voltar", None, pos_jogador, direcao_atual
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    return "voltar", None, pos_jogador, direcao_atual
                
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
        screen.fill((0, 0, 0))
        desenhar_grid_montanha(screen, grid, pos_jogador, sprite_chao, sprite_blocantes, sprite_monstro, monstros_sala, sprites_personagem, direcao_atual)
        mensagem = "Pressione 'q' para voltar ao menu de ação"
        text = font.render(mensagem, True, (255, 255, 0))
        screen.blit(text, ((screen.get_width() - text.get_width()) // 2, altura * CELL_SIZE + 5))
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()
    return "voltar", None, pos_jogador, direcao_atual

if __name__ == "__main__":
    # Exemplo de uso com dados fictícios de sala
    sala_teste = {
        'nome': 'Montanha Nevada',
        'conexao_norte': None,
        'conexao_sul': 1,
        'conexao_leste': None,
        'conexao_oeste': None
    }
    main_grid_pygame_montanha(sala_teste)