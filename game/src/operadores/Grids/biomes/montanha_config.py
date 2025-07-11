from ..common.sprite_loader import SpriteLoader

# Configuração do bioma Montanha Nevada
MONTANHA_CONFIG = {
    'nome': 'Montanha Nevada',
    'monster_emoji': '🧌', 
    'sprites': {
        'chao': {
            'path': SpriteLoader.get_asset_path('image.png'),
            'rect': (0, 200, 50, 50)
        },
        'blocante1': {
            'path': SpriteLoader.get_asset_path('blocante_neve.png'),
            'rect': (0, 0, 120, 123)
        },
        'blocante2': {
            'path': SpriteLoader.get_asset_path('arvores.png'),
            'rect': (128, 0, 63, 78) 
        },
        'blocante3': {
            'path': SpriteLoader.get_asset_path('pedras.png'),
            'rect': (5, 72, 35, 33) 
        },
        'blocante4': {
            'path': SpriteLoader.get_asset_path('pedras.png'),
            'rect': (240, 69, 43, 39)
        },
        'monster': {
            'path': SpriteLoader.get_asset_path('troll.png'),
            'rect': (0, 0, 52, 52)
        }
    },
    'colors': {
        'player': (0, 191, 255), 
        'monster': (255, 0, 0),
        'block': (100, 100, 100)
    }
}
