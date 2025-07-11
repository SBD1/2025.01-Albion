import pygame
from .common.grid_engine import GridEngine
from .biomes.montanha_config import MONTANHA_CONFIG

def main_grid_pygame_montanha(nome_sala="Montanha Nevada", sprites_personagem=None, direcao_atual="baixo", screen=None):
    """
    Função principal para renderizar e controlar o grid da montanha.
    Refatorada para usar o GridEngine comum.
    """
    engine = GridEngine(MONTANHA_CONFIG)
    return engine.run_grid(nome_sala, sprites_personagem, direcao_atual, screen)

