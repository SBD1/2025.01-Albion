from simple_term_menu import TerminalMenu
import sys
import getpass
from game.src.ascii_art import albion_ascii,encerrar_ascii
from game.src.operadores.Usuario.register import register_user
from game.src.operadores.Usuario.login import login
from game.src.database import criar_cursor
from game.src.limpar_tela import limpar_tela
def menu_usuario():
    
    opcoes_login = ["Entrar", "Criar Conta", "Sair"]
    logar = TerminalMenu(opcoes_login,
                        menu_cursor_style=("fg_green", "bold"),
                        menu_highlight_style=("fg_green", "bold"),
                        clear_screen=False) 

    while True:
        print(albion_ascii)

        cursor = criar_cursor()
        opcao = logar.show()
        if opcao == 0:
            limpar_tela()
            username = input("Digite seu nome de usuário: ")
            password = getpass.getpass("Digite sua senha: ")
            limpar_tela()
            id_usuario = login(username, password, cursor)
            if id_usuario:
                return id_usuario, username
            
        elif opcao == 1:
            limpar_tela()
            username = input("Digite seu nome de usuário: ")
            password = getpass.getpass("Digite sua senha: ")
            limpar_tela()
            register_user(username, password, cursor)
            return None, username

        elif opcao == 2:
            limpar_tela()
            print(encerrar_ascii)
            sys.exit()
