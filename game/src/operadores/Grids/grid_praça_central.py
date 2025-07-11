import pygame
from .common.grid_engine import GridEngine
from .biomes.praca_config import PRACA_CONFIG

def main_grid_pygame_praca(nome_sala="Praça Central", sprites_personagem=None, direcao_atual="baixo", screen=None):
    """
    Função principal para renderizar e controlar o grid da praça central.
    Refatorada para usar o GridEngine comum.
    """
    engine = GridEngine(PRACA_CONFIG)
    return engine.run_grid(nome_sala, sprites_personagem, direcao_atual, screen)
