import pygame
import os

# Configurações dos sprites do personagem
CELL_SIZE = 32
SPRITE_PATH_PERSONAGEM = os.path.join(os.path.dirname(__file__), '../../../assets/main.png')

# Retângulos para cada direção do personagem
PERSONAGEM_CIMA_RECT = pygame.Rect(17, 15, 30, 46)
PERSONAGEM_ESQUERDA_RECT = pygame.Rect(22, 79, 20, 46)
PERSONAGEM_BAIXO_RECT = pygame.Rect(17, 143, 30, 46)
PERSONAGEM_DIREITA_RECT = pygame.Rect(22, 206, 20, 46)

def carregar_sprites_personagem():
    """Carrega e redimensiona todos os sprites do personagem para cada direção."""
    try:
        # Garante que pygame está inicializado
        if not pygame.get_init():
            pygame.init()
        if not pygame.display.get_init():
            pygame.display.set_mode((32, 32))  # Modo temporário mínimo
            
        sprite_sheet = pygame.image.load(SPRITE_PATH_PERSONAGEM).convert_alpha()
        
        sprites = {}
        
        # Sprite para cima
        sprite_cima = pygame.Surface((PERSONAGEM_CIMA_RECT.width, PERSONAGEM_CIMA_RECT.height), pygame.SRCALPHA)
        sprite_cima.blit(sprite_sheet, (0, 0), PERSONAGEM_CIMA_RECT)
        sprites['cima'] = pygame.transform.scale(sprite_cima, (CELL_SIZE, CELL_SIZE))
        
        # Sprite para esquerda
        sprite_esquerda = pygame.Surface((PERSONAGEM_ESQUERDA_RECT.width, PERSONAGEM_ESQUERDA_RECT.height), pygame.SRCALPHA)
        sprite_esquerda.blit(sprite_sheet, (0, 0), PERSONAGEM_ESQUERDA_RECT)
        sprites['esquerda'] = pygame.transform.scale(sprite_esquerda, (CELL_SIZE, CELL_SIZE))
        
        # Sprite para baixo
        sprite_baixo = pygame.Surface((PERSONAGEM_BAIXO_RECT.width, PERSONAGEM_BAIXO_RECT.height), pygame.SRCALPHA)
        sprite_baixo.blit(sprite_sheet, (0, 0), PERSONAGEM_BAIXO_RECT)
        sprites['baixo'] = pygame.transform.scale(sprite_baixo, (CELL_SIZE, CELL_SIZE))
        
        # Sprite para direita
        sprite_direita = pygame.Surface((PERSONAGEM_DIREITA_RECT.width, PERSONAGEM_DIREITA_RECT.height), pygame.SRCALPHA)
        sprite_direita.blit(sprite_sheet, (0, 0), PERSONAGEM_DIREITA_RECT)
        sprites['direita'] = pygame.transform.scale(sprite_direita, (CELL_SIZE, CELL_SIZE))
        
        return sprites
        
    except pygame.error as e:
        print(f"Erro ao carregar sprites do personagem: {e}")
        # Garante que pygame está inicializado para fallback
        if not pygame.get_init():
            pygame.init()
        if not pygame.display.get_init():
            pygame.display.set_mode((32, 32))  # Modo temporário mínimo
        # Retorna sprites de fallback (retângulos coloridos)
        fallback_sprites = {}
        for direcao in ['cima', 'esquerda', 'baixo', 'direita']:
            fallback = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            fallback.fill((0, 255, 0))  # Verde como fallback
            fallback_sprites[direcao] = fallback
        return fallback_sprites
    except Exception as e:
        print(f"Erro geral ao carregar sprites do personagem: {e}")
        # Garante que pygame está inicializado para fallback
        if not pygame.get_init():
            pygame.init()
        if not pygame.display.get_init():
            pygame.display.set_mode((32, 32))  # Modo temporário mínimo
        # Retorna sprites de fallback (retângulos coloridos)
        fallback_sprites = {}
        for direcao in ['cima', 'esquerda', 'baixo', 'direita']:
            fallback = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            fallback.fill((0, 255, 0))  # Verde como fallback
            fallback_sprites[direcao] = fallback
        return fallback_sprites

def desenhar_personagem_sprite(screen, pos_jogador, direcao_atual, sprites_personagem):
    """Desenha o sprite do personagem na direção correta."""
    if sprites_personagem and direcao_atual in sprites_personagem:
        x, y = pos_jogador[1] * CELL_SIZE, pos_jogador[0] * CELL_SIZE
        screen.blit(sprites_personagem[direcao_atual], (x, y))
    else:
        # Fallback para desenho com retângulo se sprites não estiverem disponíveis
        x, y = pos_jogador[1] * CELL_SIZE, pos_jogador[0] * CELL_SIZE
        pygame.draw.rect(screen, (0, 255, 0), (x, y, CELL_SIZE, CELL_SIZE), 3)
