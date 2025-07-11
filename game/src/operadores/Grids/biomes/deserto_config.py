from ..common.sprite_loader import SpriteLoader

# Configuração do bioma Deserto Escaldante
DESERTO_CONFIG = {
    'nome': 'Deserto Escaldante',
    'monster_emoji': '🧟‍♂️', 
    'sprites': {
        'chao': {
            'path': SpriteLoader.get_asset_path('base_out_atlas.png'),
            'rect': (599, 84, 61, 56)
        },
        'blocante1': {
            'path': SpriteLoader.get_asset_path('base_out_atlas.png'),
            'rect': (0, 254, 31, 32)
        },
        'blocante2': {
            'path': SpriteLoader.get_asset_path('terrain_atlas.png'),
            'rect': (833, 688, 61, 46)
        },
        'blocante3': {
            'path': SpriteLoader.get_asset_path('base_out_atlas.png'),
            'rect': (319, 223, 33, 32) 
        },
        'blocante4': {
            'path': SpriteLoader.get_asset_path('terrain_atlas.png'),
            'rect': (835, 928, 25, 53) 
        },
        'monster': {
            'path': SpriteLoader.get_asset_path('monster.png'),
            'rect': (54, 53, 163, 107) 
        }
    },
    'colors': {
        'player': (255, 0, 0), 
        'monster': (255, 0, 0),
        'block': (100, 100, 100)
    }
}
