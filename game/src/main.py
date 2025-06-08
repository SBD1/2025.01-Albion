import psycopg2
from psycopg2.extras import RealDictCursor
from simple_term_menu import TerminalMenu
import os
from ascii_art import albion_ascii, encerrar_ascii
import getpass
from limpar_tela import limpar_tela
from operadores.register import register_user

def logar_usuario():
    opcoes_login = ["Entrar", "Criar Conta", "Sair"]
    logar = TerminalMenu(opcoes_login,
                        menu_cursor_style=("fg_green", "bold"),
                        menu_highlight_style=("fg_green", "bold"),
                        clear_screen=False) 

    while True:
        opcao = logar.show()
        if opcao == 0:
            limpar_tela()
            username = input("Digite seu nome de usuário: ")
            password = getpass.getpass("Digite sua senha: ")
            limpar_tela()
            id_usuario = login(username, password)
        elif opcao == 1:
            limpar_tela()
            username = input("Digite seu nome de usuário: ")
            password = getpass.getpass("Digite sua senha: ")
            limpar_tela()
            id_usuario = register_user(username, password)
        elif opcao == 2:
            limpar_tela()
            print(encerrar_ascii)
            break


def main():
    print(albion_ascii)
    logar_usuario()
    
if __name__ == "__main__":
    main()