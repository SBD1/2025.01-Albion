encerrar_ascii = r"""
   ____   _            _                    _                                 _                             _ 
  / __ \ | |          (_)                  | |                               (_)                           | |
 | |  | || |__   _ __  _   __ _   __ _   __| |  ___    _ __    ___   _ __     _   ___    __ _   __ _  _ __ | |
 | |  | || '_ \ | '__|| | / _` | / _` | / _` | / _ \  | '_ \  / _ \ | '__|   | | / _ \  / _` | / _` || '__|| |
 | |__| || |_) || |   | || (_| || (_| || (_| || (_) | | |_) || (_) || |      | || (_) || (_| || (_| || |   |_|
  \____/ |_.__/ |_|   |_| \__, | \__,_| \__,_| \___/  | .__/  \___/ |_|      | | \___/  \__, | \__,_||_|   (_)
                           __/ |                      | |                   _/ |         __/ |                
                          |___/                       |_|                  |__/         |___/                   
"""
albion_ascii = r"""
            _  _      _                
     /\    | || |    (_)               
    /  \   | || |__   _   ___   _ __   
   / /\ \  | || '_ \ | | / _ \ | '_ \  
  / ____ \ | || |_) || || (_) || | | | 
 /_/    \_\|_||_.__/ |_| \___/ |_| |_| 
"""

praça_central = """ 
                            ╔═══════════════════╗
                            ║ Campos Congelados ║
                            ╚═════════╦═════════╝
                                      ↑ 
                     ╔════════════════╩══════════════╗
                     ║                               ║
   Pântano Sombrio ← ║      ██  PRAÇA CENTRAL  ██    ║ → Deserto Escaldante 
                     ║                               ║
                     ╚════════════════╦══════════════╝
                                      ↓ 
                            ╔═════════╩═════════╗
                            ║  Caverna Sombria  ║
                            ╚═══════════════════╝
"""

campos_congelados = """ 
                            ╔══════════════════╗
                            ║  Montanha Nevada ║
                            ╚═════════╦════════╝
                                      ↑ 
                     ╔════════════════╩══════════════╗
                     ║         ❄️ ❄️ ❄️ ❄️ ❄️ ❄️ ❄️ ❄️      ║
                     ║        CAMPOS CONGELADOS      ║ → Floresta do Leste 
                     ║         ❄️ ❄️ ❄️ ❄️ ❄️ ❄️ ❄️ ❄️      ║
                     ╚════════════════╦══════════════╝
                                      ↓ 
                            ╔═════════╩════════╗
                            ║   Praça Central  ║
                            ╚══════════════════╝
"""

caverna_sombria = """
                           ╔═══════════════════╗
                           ║   Praça Central   ║
                           ╚══════════╦════════╝
                                      ↑ 
                     ╔════════════════╩══════════════╗
                     ║          🕳️ 🕳️ 🕳️ 🕳️ 🕳️ 🕳️ 🕳️        ║
                     ║         CAVERNA SOMBRIA       ║
                     ║          💀💀💀💀💀💀         ║
                     ╚════════════════╦══════════════╝
                                      ↓ 
                             ╔════════╩═════════╗
                             ║  Ruínas Antigas  ║
                             ╚══════════════════╝
"""

deserto_escaldante = """        
                     ╔════════════════════════════╗
                     ║                            ║
     Praça Central ← ║     DESERTO ESCALDANTE     ║
                     ║        🔥🔥🔥🔥🔥🔥        ║
                     ╚═══════════════╦════════════╝
                                     ↓ 
                            ╔════════╩═════════╗
                            ║  Ruínas Antigas  ║
                            ╚══════════════════╝
"""

pantano_sombrio = """        
                     ╔════════════════════════════╗
                     ║                                 ║
                     ║       PÂNTANO SOMBRIO      ║ → Praça Central 
                     ║        ☠️ ☠️ ☠️ ☠️ ☠️ ☠️        ║
                     ╚════════════════════════════╝
"""

montanha_nevada = """        
                     ╔════════════════════════════╗
                     ║     ⛰️ ⛰️ ⛰️ ⛰️ ⛰️ ⛰️      ║
                     ║     MONTANHA NEVADA       ║
                     ║     ❄️ ❄️ ❄️ ❄️ ❄️ ❄️      ║
                     ╚═══════════════╦════════════╝
                                     ↓ 
                            ╔════════╩═════════╗
                            ║ Campos Congelados║
                            ╚══════════════════╝
"""

floresta_do_leste = """        
                     ╔════════════════════════════╗
                     ║     🌲🌲🌲🌲🌲🌲🌲     ║
 Campos Congelados ← ║    FLORESTA DO LESTE      ║
                     ║     🌳🌳🌳🌳🌳🌳🌳     ║
                     ╚════════════════════════════╝
"""

ruinas_antigas = """        
                         ╔══════════════════╗
                         ║ Caverna  Sombria ║
                         ╚═════════╦════════╝
                                   ↑ 
                     ╔═════════════╩══════════════╗
                     ║        🏛️ 🏛️ 🏛️ 🏛️ 🏛️ 🏛️         ║
                     ║       RUÍNAS ANTIGAS       ║ → Deserto Escaldante 
                     ║                            ║
                     ╚════════════════════════════╝
"""

salas = {
    "Praça Central": praça_central,
    "Campos Congelados": campos_congelados,
    "Caverna Sombria": caverna_sombria,
    "Deserto Escaldante": deserto_escaldante,
    "Pântano Sombrio": pantano_sombrio,
    "Montanha Nevada": montanha_nevada,
    "Floresta do Leste": floresta_do_leste,
    "Ruínas Antigas": ruinas_antigas,
}

salas_conexoes = {
    "Praça Central": praça_central,
    "Campos Congelados": campos_congelados,
    "Caverna Sombria": caverna_sombria,
    "Deserto Escaldante": deserto_escaldante,
    "Pântano Sombrio": pantano_sombrio,
    "Montanha Nevada": montanha_nevada,
    "Floresta do Leste": floresta_do_leste,
    "Ruínas Antigas": ruinas_antigas,
}

import random

def gerar_grid_personalizado_com_saidas(tamanho_vertical, tamanho_horizontal, elemento_blocante, elemento_blocante2, conexoes, emoji):
    grid = [[" " for _ in range(tamanho_horizontal)] for _ in range(tamanho_vertical)]
    max_montros=15

    # Adicionar bordas
    for i in range(tamanho_vertical):
        grid[i][0] = elemento_blocante2
        grid[i][tamanho_horizontal - 1] = elemento_blocante2
    for j in range(tamanho_horizontal):
        grid[0][j] = elemento_blocante2
        grid[tamanho_vertical - 1][j] = elemento_blocante2

    # Adicionar saídas com base nas conexões
    saidas = []
    if conexoes.get("norte"):
        grid[0][tamanho_horizontal // 2] = " "
        saidas.append((0, tamanho_horizontal // 2))
    if conexoes.get("sul"):
        grid[tamanho_vertical - 1][tamanho_horizontal // 2] = " "
        saidas.append((tamanho_vertical - 1, tamanho_horizontal // 2))
    if conexoes.get("leste"):
        grid[tamanho_vertical // 2][tamanho_horizontal - 1] = " "
        saidas.append((tamanho_vertical // 2, tamanho_horizontal - 1))
    if conexoes.get("oeste"):
        grid[tamanho_vertical // 2][0] = " "
        saidas.append((tamanho_vertical // 2, 0))

    # Distribuir elementos blocantes aleatoriamente
    for _ in range((tamanho_vertical * tamanho_horizontal) // 15):
        while True:
            x = random.randint(2, tamanho_vertical - 3)
            y = random.randint(2, tamanho_horizontal - 3)
            if (x, y) not in saidas and grid[x][y] == " ":
                grid[x][y] = elemento_blocante
                break

    # Distribuir monstros aleatoriamente, evitando elementos blocantes e saídas
    monstros = []
    for _ in range(max_montros):
        while True:
            x, y = random.randint(2, tamanho_vertical - 2), random.randint(2, tamanho_horizontal - 2)
            if (x, y) not in saidas and grid[x][y] == " ":
                grid[x][y] = f"{emoji}"
                monstros.append((x, y))
                break

    return grid, monstros


grids = {
    "Praça Central": [
"######################### ########################",
"#  ██████████                        ██████████  #",
"#  █        █                        █        █  #",
"#  █                                          █  #",
"#  █        █                        █        █  #",
"#  ██████████                        ██████████  #",
"#                                                #",
"                                                  ",
"#                                                #",
"#  ██████████                        ██████████  #",
"#  █        █                        █        █  #",
"#  █                                          █  #",
"#  █        █                        █        █  #",
"#  ██████████                        ██████████  #",
"######################### ########################"],

    "Campos Congelados": gerar_grid_personalizado_com_saidas(15, 50, "🧊","❄️", {"norte": True, "sul": True, "leste": True, "oeste": False}, "🐻‍❄️"),
    "Caverna Sombria": gerar_grid_personalizado_com_saidas(15, 50, "🪨","🕳️", {"norte": True, "sul": True, "leste": False, "oeste": True},   "🧛"),
    "Deserto Escaldante": gerar_grid_personalizado_com_saidas(15, 50,"🟤","🔥", {"norte": False, "sul": True, "leste": True, "oeste": True}, "🧟‍♂️"),
    "Floresta do Leste": gerar_grid_personalizado_com_saidas(15, 50,"🌳","🌲", {"norte": False, "sul": False, "leste": False, "oeste": True},"👺"),
    "Montanha Nevada": gerar_grid_personalizado_com_saidas(15, 50, "❄️", "⛰️", {"norte": False, "sul": True, "leste": False, "oeste": False},"🧌"),
    "Pântano Sombrio": gerar_grid_personalizado_com_saidas(15, 50,"🍄","🟢", {"norte": False, "sul": False, "leste": True, "oeste": False},  "🦠"),
    "Ruínas Antigas": gerar_grid_personalizado_com_saidas(15, 50,"🪨", "🏛️", {"norte": True, "sul": False, "leste": False, "oeste": True},   "🗿")
}

