import pygame
from .common.grid_engine import GridEngine
from .biomes.deserto_config import DESERTO_CONFIG

def main_grid_pygame_deserto(nome_sala="Deserto Escaldante", sprites_personagem=None, direcao_atual="baixo", screen=None):
    """
    Função principal para renderizar e controlar o grid do deserto.
    Refatorada para usar o GridEngine comum.
    """
    engine = GridEngine(DESERTO_CONFIG)
    return engine.run_grid(nome_sala, sprites_personagem, direcao_atual, screen)
