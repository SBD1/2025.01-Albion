#!/usr/bin/env python3
"""
Script para adicionar sprites de monstros em todos os grids do jogo Albion.
Coordenadas do monstro: (54, 53, 217-54, 160-53)
"""

import os
import re

# Lista de grids a serem modificados
GRIDS = [
    "grid_deserto.py",
    "grid_pantano.py", 
    "grid_caverna.py",
    "grid_praça_central.py",
    "grid_campos_congelados.py",
    "grid_montanha.py"
]

BASE_PATH = "/home/anjos/documentos/github/2025.01-Albion/game/src/operadores/Grids"

def add_monster_support_to_grid(filepath):
    """Adiciona suporte a sprites de monstros em um arquivo de grid."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Adicionar SPRITE_PATH_MONSTER e MONSTER_RECT se não existir
    if 'SPRITE_PATH_MONSTER' not in content:
        # Encontrar onde adicionar as novas constantes
        sprite_path_pattern = r'(SPRITE_PATH.*?= os\.path\.join.*?\n)'
        match = re.search(sprite_path_pattern, content)
        if match:
            insertion_point = match.end()
            monster_constants = 'SPRITE_PATH_MONSTER = os.path.join(os.path.dirname(__file__), \'../../../assets/monster.png\')\n'
            content = content[:insertion_point] + monster_constants + content[insertion_point:]
    
    if 'MONSTER_RECT' not in content:
        # Adicionar MONSTER_RECT após outros RECTs
        rect_pattern = r'(.*_RECT = pygame\.Rect.*?\n)'
        matches = list(re.finditer(rect_pattern, content))
        if matches:
            insertion_point = matches[-1].end()
            monster_rect = 'MONSTER_RECT = pygame.Rect(54, 53, 217-54, 160-53)  # Coordenadas do monstro\n'
            content = content[:insertion_point] + monster_rect + content[insertion_point:]
    
    # 2. Adicionar função carregar_sprite_monstro se não existir
    if 'def carregar_sprite_monstro' not in content:
        # Encontrar onde adicionar a função (após outras funções de carregar sprite)
        function_pattern = r'(def carregar_sprite.*?\n(?:.*?\n)*?.*?return.*?\n)'
        matches = list(re.finditer(function_pattern, content, re.MULTILINE))
        if matches:
            insertion_point = matches[-1].end()
            monster_function = '''
def carregar_sprite_monstro():
    """Carrega o sprite do monstro usando as coordenadas especificadas."""
    try:
        sprite_sheet = pygame.image.load(SPRITE_PATH_MONSTER).convert_alpha()
        monster_sprite = pygame.Surface((MONSTER_RECT.width, MONSTER_RECT.height), pygame.SRCALPHA)
        monster_sprite.blit(sprite_sheet, (0, 0), MONSTER_RECT)
        return pygame.transform.scale(monster_sprite, (CELL_SIZE, CELL_SIZE))
    except pygame.error as e:
        print(f"Erro ao carregar sprite do monstro: {e}")
        # Retorna um sprite vermelho como fallback
        fallback = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        fallback.fill((255, 0, 0))
        return fallback
'''
            content = content[:insertion_point] + monster_function + content[insertion_point:]
    
    # 3. Modificar função de desenhar para incluir monstros
    # Procurar por função def desenhar_grid_*
    desenhar_pattern = r'def desenhar_grid_\w+\([^)]+\):'
    match = re.search(desenhar_pattern, content)
    if match:
        # Encontrar o final da assinatura da função
        func_start = match.start()
        func_sig_end = match.end()
        
        # Modificar assinatura se necessário
        if 'monstros_sala' not in content[func_start:func_sig_end+100]:
            old_sig = content[func_start:func_sig_end]
            if 'sprite_monstro' not in old_sig:
                new_sig = old_sig.rstrip(':') + ', sprite_monstro=None, monstros_sala=None):'
            else:
                new_sig = old_sig.rstrip(':').replace(')', ', monstros_sala=None)')
            content = content[:func_start] + new_sig + content[func_sig_end:]
        
        # Adicionar código para desenhar monstros
        if 'Desenha os monstros nas posições da sala' not in content:
            # Procurar por onde adicionar o código de monstros (antes do jogador)
            jogador_pattern = r'(\s*# .*[Jj]ogador.*?\n.*?pygame\.draw\.rect.*?\n)'
            match_jogador = re.search(jogador_pattern, content)
            if match_jogador:
                insertion_point = match_jogador.start()
                monster_code = '''
    # Desenha os monstros nas posições da sala
    if sprite_monstro and monstros_sala:
        for monstro_pos in monstros_sala:
            if len(monstro_pos) >= 2:
                mx, my = monstro_pos[0], monstro_pos[1]
                if 0 <= mx < altura and 0 <= my < largura:
                    xm, ym = my * CELL_SIZE, mx * CELL_SIZE
                    screen.blit(sprite_monstro, (xm, ym))
'''
                content = content[:insertion_point] + monster_code + content[insertion_point:]
    
    # 4. Modificar função main_grid_pygame_* para carregar sprite do monstro
    main_pattern = r'def main_grid_pygame_\w+\([^)]*\):'
    match = re.search(main_pattern, content)
    if match:
        # Procurar por onde adicionar sprite_monstro
        sprite_load_pattern = r'(\s*sprite_\w+ = carregar_sprite_.*?\n)'
        matches = list(re.finditer(sprite_load_pattern, content))
        if matches:
            insertion_point = matches[-1].end()
            monster_sprite_load = '    sprite_monstro = carregar_sprite_monstro()\n'
            if 'sprite_monstro = carregar_sprite_monstro()' not in content:
                content = content[:insertion_point] + monster_sprite_load + content[insertion_point:]
        
        # Modificar carregamento de grid_data para incluir monstros
        grid_data_pattern = r'(\s*grid_data = grids\[nome_sala\]\s*\n\s*if isinstance\(grid_data.*?\n\s*grid = .*?\n\s*else:\s*\n\s*grid, _ = grid_data)'
        match_grid = re.search(grid_data_pattern, content, re.MULTILINE)
        if match_grid:
            new_grid_code = '''    grid_data = grids[nome_sala]
    if isinstance(grid_data, list) and isinstance(grid_data[0], str):
        grid = [list(l) for l in grid_data]
        monstros_sala = []
    else:
        grid, monstros_sala = grid_data'''
            content = content[:match_grid.start()] + new_grid_code + content[match_grid.end():]
        
        # Modificar chamada da função de desenhar
        desenhar_call_pattern = r'(\s*desenhar_grid_\w+\([^)]+\))'
        match_call = re.search(desenhar_call_pattern, content)
        if match_call and 'monstros_sala' not in match_call.group():
            old_call = match_call.group()
            if 'sprite_monstro' not in old_call:
                new_call = old_call.rstrip(')') + ', sprite_monstro, monstros_sala)'
            else:
                new_call = old_call.rstrip(')') + ', monstros_sala)'
            content = content[:match_call.start()] + new_call + content[match_call.end():]
    
    # Salvar arquivo modificado
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Arquivo {filepath} modificado com sucesso!")

# Executar modificações em todos os grids
for grid_file in GRIDS:
    filepath = os.path.join(BASE_PATH, grid_file)
    if os.path.exists(filepath):
        print(f"Modificando {grid_file}...")
        add_monster_support_to_grid(filepath)
    else:
        print(f"Arquivo {grid_file} não encontrado!")

print("Todos os grids foram modificados!")
