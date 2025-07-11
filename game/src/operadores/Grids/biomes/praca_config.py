from ..common.sprite_loader import SpriteLoader

# Configuração do bioma Praça Central
PRACA_CONFIG = {
    'nome': 'Praça Central',
    'monster_emoji': '👮', 
    'sprites': {
        'chao': {
            'path': SpriteLoader.get_asset_path('base_out_atlas.png'),
            'rect': (607, 991, 32, 27) 
        },
        'blocante1': {
            'path': SpriteLoader.get_asset_path('base_out_atlas.png'),
            'rect': (640, 480, 32, 32)
        },
        'blocante2': {
            'path': SpriteLoader.get_asset_path('base_out_atlas.png'),
            'rect': (783, 327, 24, 24)
        },
        'blocante3': {
            'path': SpriteLoader.get_asset_path('base_out_atlas.png'),
            'rect': (783, 327, 24, 24)
        },
        'blocante4': {
            'path': SpriteLoader.get_asset_path('base_out_atlas.png'),
            'rect': (783, 327, 24, 24)
        },
        'monster': {
            'path': SpriteLoader.get_asset_path('monster.png'),
            'rect': (54, 53, 163, 107) 
        }
    },
    'colors': {
        'player': (255, 255, 255), 
        'monster': (255, 0, 0),
        'block': (100, 100, 100)
    }
}
