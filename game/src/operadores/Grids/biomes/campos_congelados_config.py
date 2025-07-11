from ..common.sprite_loader import SpriteLoader

# Configuração do bioma Campos Congelados
CAMPOS_CONGELADOS_CONFIG = {
    'nome': 'Campos Congelados',
    'monster_emoji': '🐻‍❄️',  # Emoji específico removido do grid
    'sprites': {
        'chao': {
            'path': SpriteLoader.get_asset_path('chao_neve.png'),
            'rect': (0, 0, 128, 128)
        },
        'blocante1': {
            'path': SpriteLoader.get_asset_path('arvores.png'),
            'rect': (180, 79, 54, 63)  # 234-180, 142-79
        },
        'blocante2': {
            'path': SpriteLoader.get_asset_path('arvores.png'),
            'rect': (311, 80, 49, 61)  # 360-311, 141-80
        },
        'blocante3': {
            'path': SpriteLoader.get_asset_path('arvores.png'),
            'rect': (180, 80, 55, 63)  # 235-180, 143-80
        },
        'blocante4': {
            'path': SpriteLoader.get_asset_path('arvores.png'),
            'rect': (495, 143, 30, 31)  # 525-495, 174-143
        },
        'monster': {
            'path': SpriteLoader.get_asset_path('yeti.png'),
            'rect': (8, 8, 60, 60)
        }
    },
    'colors': {
        'player': (139, 69, 19),  # Marrom para o jogador na neve
        'monster': (255, 0, 0),
        'block': (100, 100, 100)
    }
}
