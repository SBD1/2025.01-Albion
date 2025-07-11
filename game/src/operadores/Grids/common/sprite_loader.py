import pygame
import os

class SpriteLoader:
    """Classe utilitária para carregar sprites de forma padronizada."""
    
    CELL_SIZE = 58
    
    @staticmethod
    def load_sprite(sprite_path, rect, cell_size=None):
        """
        Carrega um sprite específico de uma sprite sheet.
        
        Args:
            sprite_path (str): Caminho para o arquivo de sprite
            rect (pygame.Rect ou tuple): Retângulo para recorte do sprite
            cell_size (int): Tamanho da célula (padrão: CELL_SIZE)
            
        Returns:
            pygame.Surface: Sprite carregado e redimensionado
        """
        if cell_size is None:
            cell_size = SpriteLoader.CELL_SIZE
            
        try:
            sprite_sheet = pygame.image.load(sprite_path)
            if pygame.display.get_surface() is not None:
                sprite_sheet = sprite_sheet.convert_alpha()

            if isinstance(rect, tuple):
                if len(rect) == 4:
                    rect = pygame.Rect(rect)
                else:
                    raise ValueError("Tuple deve ter 4 elementos (x, y, width, height)")
            
            sprite = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            sprite.blit(sprite_sheet, (0, 0), rect)
            return pygame.transform.scale(sprite, (cell_size, cell_size))
            
        except pygame.error as e:
            print(f"Erro ao carregar sprite de {sprite_path}: {e}")
            fallback = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
            fallback.fill((255, 0, 255))  
            return fallback
    
    @staticmethod
    def load_biome_sprites(biome_config):
        """
        Carrega todos os sprites de um bioma baseado na configuração.
        
        Args:
            biome_config (dict): Configuração do bioma
            
        Returns:
            dict: Dicionário com todos os sprites carregados
        """
        sprites = {}
        
        # Carrega sprite do chão
        if 'chao' in biome_config['sprites']:
            config = biome_config['sprites']['chao']
            sprites['chao'] = SpriteLoader.load_sprite(config['path'], config['rect'])
        
        # Carrega sprites dos blocantes
        sprites['blocantes'] = []
        i = 1
        while f'blocante{i}' in biome_config['sprites']:
            config = biome_config['sprites'][f'blocante{i}']
            sprite = SpriteLoader.load_sprite(config['path'], config['rect'])
            sprites['blocantes'].append(sprite)
            i += 1
        
        # Carrega sprite do monstro
        if 'monster' in biome_config['sprites']:
            config = biome_config['sprites']['monster']
            sprites['monster'] = SpriteLoader.load_sprite(config['path'], config['rect'])
        
        return sprites
    
    @staticmethod
    def get_asset_path(asset_name):
        """
        Constrói o caminho para um asset baseado na estrutura do projeto.
        
        Args:
            asset_name (str): Nome do arquivo de asset
            
        Returns:
            str: Caminho completo para o asset
        """
        return os.path.join(os.path.dirname(__file__), '../../../../assets', asset_name)
