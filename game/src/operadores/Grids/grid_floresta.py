import pygame
from .common.grid_engine import GridEngine
from .biomes.floresta_config import FLORESTA_CONFIG

def main_grid_pygame_floresta(nome_sala="Floresta do Leste", sprites_personagem=None, direcao_atual="baixo", screen=None):
    """
    Função principal para renderizar e controlar o grid da floresta.
    Refatorada para usar o GridEngine comum.
    """
    engine = GridEngine(FLORESTA_CONFIG)
    return engine.run_grid(nome_sala, sprites_personagem, direcao_atual, screen)