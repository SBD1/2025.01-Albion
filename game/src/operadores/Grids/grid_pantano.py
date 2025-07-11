import pygame
from .common.grid_engine import GridEngine
from .biomes.pantano_config import PANTANO_CONFIG

def main_grid_pygame_pantano(nome_sala="Pântano Sombrio", sprites_personagem=None, direcao_atual="baixo", screen=None):
    """
    Função principal para renderizar e controlar o grid do pântano.
    Refatorada para usar o GridEngine comum.
    """
    engine = GridEngine(PANTANO_CONFIG)
    return engine.run_grid(nome_sala, sprites_personagem, direcao_atual, screen)
