from ..common.sprite_loader import SpriteLoader

# Configuração do bioma Ruínas Antigas
RUINAS_CONFIG = {
    'nome': 'Ruínas Antigas',
    'monster_emoji': '🗿', 
    'sprites': {
        'chao': {
            'path': SpriteLoader.get_asset_path('terrain_atlas.png'),
            'rect': (607, 704, 33, 31) 
        },
        'blocante1': {
            'path': SpriteLoader.get_asset_path('terrain_atlas.png'),
            'rect': (608, 484, 31, 92)  
        },
        'blocante2': {
            'path': SpriteLoader.get_asset_path('terrain_atlas.png'),
            'rect': (865, 851, 58, 41)
        },
        'blocante3': {
            'path': SpriteLoader.get_asset_path('terrain_atlas.png'),
            'rect': (447, 383, 32, 96) 
        },
        'monster': {
            'path': SpriteLoader.get_asset_path('golem.png'),
            'rect': (0, 0, 93, 71)
        }
    },
    'colors': {
        'player': (255, 0, 0),  
        'monster': (255, 0, 0),
        'block': (100, 100, 100)
    }
}
