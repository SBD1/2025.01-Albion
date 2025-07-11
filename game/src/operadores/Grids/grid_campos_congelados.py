import pygame
from .common.grid_engine import GridEngine
from .biomes.campos_congelados_config import CAMPOS_CONGELADOS_CONFIG

def main_grid_pygame_neve(nome_sala="Campos Congelados", sprites_personagem=None, direcao_atual="baixo", screen=None):
    """
    Função principal para renderizar e controlar o grid dos campos congelados.
    Refatorada para usar o GridEngine comum.
    """
    engine = GridEngine(CAMPOS_CONGELADOS_CONFIG)
    return engine.run_grid(nome_sala, sprites_personagem, direcao_atual, screen)
