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
#def montar_mapa(x,y):
#    molde_15x15 = []
#    for i in range(11):
#        molde_15x15.append("\n")
#        molde_15x15.append("║")
#        temp = []
#        for j in range(25):
#            if i == 0 or i == 10:
#                molde_15x15.append("═")
#            else:
#                molde_15x15.append(" ")
#        molde_15x15.append("║")
#
#    molde_15x15[14] = "⬆️"
#    molde_15x15[6*19] = "→"
#    molde_15x15[185] = "➡️"
#    molde_15x15[294] = "⬇️"
#    molde_15x15[x*y] = "♥"
#    mapa = "".join(molde_15x15)
#    
#    print(mapa)
    
#def conexoes_salas(norte,oeste,sul,leste):
#    if norte == True:
#        molde_15x15[5] = "↑"
#    if oeste == True:
#        molde_15x15[5*17] = "→"
#    if sul == True:
#        molde_15x15[17*9] = "→"
#
#    if leste == True:

#montar_mapa(5,20)