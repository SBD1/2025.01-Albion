import pygame
from .common.grid_engine import GridEngine
from .biomes.caverna_config import CAVERNA_CONFIG

def main_grid_pygame_caverna(nome_sala="Caverna Sombria", sprites_personagem=None, direcao_atual="baixo", screen=None):
    """
    Função principal para renderizar e controlar o grid da caverna.
    Refatorada para usar o GridEngine comum.
    """
    engine = GridEngine(CAVERNA_CONFIG)
    return engine.run_grid(nome_sala, sprites_personagem, direcao_atual, screen)
