from game.src.operadores.Usuario.menu_usuario import menu_usuario
from game.src.operadores.Personagem.menu_personagens import menu_personagens
from game.src.operadores.Personagem.selecionar_personagem import selecionar_personagem
from game.src.operadores.Personagem.mover_personagem import mover_personagem
from game.src.interface import Interface
from game.src.ascii_art import TITULO_ASCII

def mostrar_boas_vindas():
    """Mostra a tela de boas-vindas do jogo."""
    Interface.limpar_tela()
    print(Interface.CORES['titulo'] + TITULO_ASCII)
    print(Interface.criar_titulo("Bem-vindo ao Albion"))
    print(Interface.CORES['info'] + "Um mundo de fantasia e aventura te aguarda!")
    print(Interface.CORES['menu'] + "Pressione ENTER para começar...")
    input()

def main():
    mostrar_boas_vindas()
    
    while True:
        Interface.limpar_tela()
        id_usuario, username = menu_usuario()
        
        if id_usuario is None:
            continue
        
        while True:
            Interface.limpar_tela()
            resultado = menu_personagens(id_usuario, username)
            
            if resultado == "voltar":
                break
            
            id_personagem = selecionar_personagem(resultado, id_usuario, username)

            if not id_personagem:
                continue

            while True:
                Interface.limpar_tela()
                result_movimento = mover_personagem(id_personagem)

                if result_movimento == "voltar":
                    break
    
if __name__ == "__main__":
    main()