from game.src.operadores.Usuario.menu_usuario import menu_usuario
from game.src.operadores.Personagem.menu_personagens import menu_personagens
from game.src.operadores.Personagem.selecionar_personagem import selecionar_personagem


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

            print(f"ID DO PERSONAGEM SELECIONADO: {id_personagem}")
    
if __name__ == "__main__":
    main()