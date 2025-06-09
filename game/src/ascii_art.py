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
                           Campos Congelados
                                   ↑ 
                     +---------------------------+
                     |                           |
   Pântano Sombrio ← |       Praça Central       | → Deserto Escaldante 
                     |                           |
                     +---------------------------+
                                   ↓ 
                             Caverna Sombria
   """
campos_congelados = """ 
                            Montanha Nevada
                                   ↑ 
                     +---------------------------+
                     |                           |
                     |     Campos Congelados     | → Floresta do Leste 
                     |                           |
                     +---------------------------+
                                   ↓ 
                              Praça Central
   """
caverna_sombria = """
                             Praça Central
                                   ↑ 
                     +---------------------------+
                     |                           |
                     |      Caverna Sombria      | 
                     |                           |
                     +---------------------------+
                                   ↓ 
                             Ruínas Antigas
   """
deserto_escaldante = """        

                     +---------------------------+
                     |                           |
     Praça Central ← |    Deserto Escaldante     | 
                     |                           |
                     +---------------------------+
                                   ↓ 
                             Ruínas Antigas
   """
pantano_sombrio = """        
                           
                     +---------------------------+
                     |                           |
                     |     Pântano Sombrio       | → Praça Central 
                     |                           |
                     +---------------------------+
                           
   """
montanha_nevada = """        
                           
                     +---------------------------+
                     |                           |
                     |     Montanha Nevada       |
                     |                           |
                     +---------------------------+
                                   ↓ 
                           Campos Congelados
   """

floresta_do_leste = """        
                           
                     +---------------------------+
                     |                           |
 Campos Congelados ← |    Floresta do Leste      | 
                     |                           |
                     +---------------------------+
"""
ruinas_antigas = """        
                            Caverna Sombria
                                   ↑ 
                     +---------------------------+
                     |                           |
                     |      Ruínas Antigas       | → Deserto Escaldante 
                     |                           |
                     +---------------------------+
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