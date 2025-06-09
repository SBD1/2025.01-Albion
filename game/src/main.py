from src.operadores.Usuario.menu_usuario import menu_usuario
from src.operadores.Personagem.menu_personagens import menu_personagens
from src.operadores.Personagem.selecionar_personagem import selecionar_personagem


def main():
    id_usuario,username = menu_usuario()
    rows_personagens = menu_personagens(id_usuario,username)
    id_personagem = selecionar_personagem(rows_personagens,id_usuario,username)
    print(f"ID DO PERSONAGEM SELECIONADO: {id_personagem}")
    
if __name__ == "__main__":
    main()