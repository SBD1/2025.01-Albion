
from game.src.database import criar_cursor
from game.src.ascii_art import salas_conexoes

def print_mapa(id_personagem):
    cursor = criar_cursor()
    cursor.execute(f"SELECT * FROM f_get_sala({id_personagem});")
    retorno = cursor.fetchone()
    # print(retorno)
    nome_sala = retorno['nome']
    
    if nome_sala in salas_conexoes:
        print(salas_conexoes[nome_sala])
    else:
        print("❌ ERRO: Mapa não disponível para esta sala.")