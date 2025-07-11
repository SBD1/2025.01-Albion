from ..common.sprite_loader import SpriteLoader

# Configuração do bioma Pântano Sombrio
PANTANO_CONFIG = {
    'nome': 'Pântano Sombrio',
    'monster_emoji': '🦠', 
    'sprites': {
        'chao': {
            'path': SpriteLoader.get_asset_path('terrain_atlas.png'),
            'rect': (209, 851, 61, 57)  
        },
        'blocante1': {
            'path': SpriteLoader.get_asset_path('arvores.png'),
            'rect': (133, 145, 39, 44)  
        },
        'blocante2': {
            'path': SpriteLoader.get_asset_path('terrain_atlas.png'),
            'rect': (383, 896, 31, 29)  
        },
        'blocante3': {
            'path': SpriteLoader.get_asset_path('terrain_atlas.png'),
            'rect': (833, 993, 28, 29)  
        },
        'blocante4': {
            'path': SpriteLoader.get_asset_path('terrain_atlas.png'),
            'rect': (193, 963, 29, 29) 
        },
        'monster': {
            'path': SpriteLoader.get_asset_path('slime.png'),
            'rect': (21, 18, 23, 23)  
        }
    },
    'colors': {
        'player': (0, 255, 0),
        'monster': (255, 0, 0),
        'block': (100, 100, 100)
    }
}
