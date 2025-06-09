from game.src.operadores.Usuario.menu_usuario import menu_usuario
from game.src.operadores.Personagem.menu_personagens import menu_personagens
from game.src.operadores.Personagem.selecionar_personagem import selecionar_personagem
from game.src.operadores.Personagem.mover_personagem import mover_personagem

def main():
    while True:
        id_usuario, username = menu_usuario()
        
        if id_usuario is None:
            continue
        
        while True:
    
            resultado = menu_personagens(id_usuario, username)
            
            if resultado == "voltar":
                break
            
            id_personagem = selecionar_personagem(resultado, id_usuario, username)

            if not id_personagem:
                continue

            while True:
                result_movimento = mover_personagem(id_personagem)

                if result_movimento == "voltar":
                    break
    
if __name__ == "__main__":
    main()