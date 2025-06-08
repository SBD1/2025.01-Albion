from simple_term_menu import TerminalMenu
import getpass
from ascii_art import albion_ascii, encerrar_ascii
from limpar_tela import limpar_tela
from operadores.criar_personagem import criar_personagem
from operadores.visualizar_personagens import visualizar_personagens
from database import criar_cursor

def menu_personagens(id_usuario):
    opcoes = ["Criar Personagem", "Visualizar Personagens", "Sair"]
    menu = TerminalMenu(
        opcoes,
        menu_cursor_style=("fg_green", "bold"),
        menu_highlight_style=("fg_green", "bold"),
        clear_screen=False
    )

    while True:
        cursor = criar_cursor()
        opcao = menu.show()
        limpar_tela()

        if opcao == 0:
            limpar_tela()
            nome_personagem = input("Digite o nome do personagem: ")
            especies = ["Zoiudo", "Draconico", "Espiritualista", "Titan"]
            menu_especie = TerminalMenu(
                especies,
                title="Selecione a espécie do seu personagem:",
                menu_cursor_style=("fg_green", "bold"),
                menu_highlight_style=("fg_green", "bold"),
                clear_screen=False
            )
            idx = menu_especie.show()
            especie_personagem = especies[idx]
            criar_personagem(id_usuario, nome_personagem, especie_personagem, cursor)
        elif opcao == 1:
            limpar_tela()
            rows_personagens = visualizar_personagens(id_usuario, cursor)
            return rows_personagens
            
        elif opcao == 2:
            limpar_tela()
            print(encerrar_ascii)
            break
