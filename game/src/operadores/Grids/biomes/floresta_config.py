from ..common.sprite_loader import SpriteLoader

# Configuração do bioma Floresta do Leste
FLORESTA_CONFIG = {
    'nome': 'Floresta do Leste',
    'monster_emoji': '👺',  
    'sprites': {
        'chao': {
            'path': SpriteLoader.get_asset_path('base_out_atlas.png'),
            'rect': (691, 84, 60, 56)
        },
        'blocante1': {
            'path': SpriteLoader.get_asset_path('base_out_atlas.png'),
            'rect': (774, 484, 76, 91)
        },
        'blocante2': {
            'path': SpriteLoader.get_asset_path('base_out_atlas.png'),
            'rect': (770, 383, 94, 80)
        },
        'blocante3': {
            'path': SpriteLoader.get_asset_path('terrain_atlas.png'),
            'rect': (416, 924, 32, 33)
        },
        'blocante4': {
            'path': SpriteLoader.get_asset_path('terrain_atlas.png'),
            'rect': (481, 896, 28, 62)
        },
        'monster': {
            'path': SpriteLoader.get_asset_path('goblin.png'),
            'rect': (9, 13, 34, 32) 
        }
    },
    'colors': {
        'player': (0, 255, 0),
        'monster': (255, 0, 0),
        'block': (100, 100, 100)
    }
}
