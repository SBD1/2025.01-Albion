from ..common.sprite_loader import SpriteLoader

# Configuração do bioma Caverna Sombria
CAVERNA_CONFIG = {
    'nome': 'Caverna Sombria',
    'monster_emoji': '🧛',  
    'sprites': {
        'chao': {
            'path': SpriteLoader.get_asset_path('base_out_atlas.png'),
            'rect': (960, 0, 60, 60)
        },
        'blocante1': {
            'path': SpriteLoader.get_asset_path('base_out_atlas.png'),
            'rect': (64, 255, 32, 32)
        },
        'blocante2': {
            'path': SpriteLoader.get_asset_path('base_out_atlas.png'),
            'rect': (64, 255, 32, 32) 
        },
        'monster': {
            'path': SpriteLoader.get_asset_path('vampiro.png'),
            'rect': (19, 17, 24, 30)  
        }
    },
    'colors': {
        'player': (255, 0, 0),
        'monster': (255, 0, 0),
        'block': (100, 100, 100)
    }
}
