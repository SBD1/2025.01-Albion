import psycopg2
from psycopg2.extras import RealDictCursor
from simple_term_menu import TerminalMenu
import os
from ascii_art import albion_ascii, encerrar_ascii
import getpass
from limpar_tela import limpar_tela
from operadores.register import register_user
from operadores.login import login
from operadores.menu_personagens import menu_personagens
from operadores.visualizar_personagens import visualizar_personagens
from operadores.selecionar_personagem import selecionar_personagem
from operadores.criar_personagem import criar_personagem
from operadores.mover_personagem import mover_personagem
from database import criar_cursor

def logar_usuario():
    opcoes_login = ["Entrar", "Criar Conta", "Sair"]
    logar = TerminalMenu(opcoes_login,
                        menu_cursor_style=("fg_green", "bold"),
                        menu_highlight_style=("fg_green", "bold"),
                        clear_screen=False) 

    while True:
        cursor = criar_cursor()
        opcao = logar.show()
        if opcao == 0:
            limpar_tela()
            username = input("Digite seu nome de usuário: ")
            password = getpass.getpass("Digite sua senha: ")
            limpar_tela()
            id_usuario = login(username, password, cursor)
            if id_usuario:
                return id_usuario
            
        elif opcao == 1:
            limpar_tela()
            username = input("Digite seu nome de usuário: ")
            password = getpass.getpass("Digite sua senha: ")
            limpar_tela()
            id_usuario = register_user(username, password, cursor)
            if id_usuario:
                return id_usuario

        elif opcao == 2:
            limpar_tela()
            print(encerrar_ascii)
            break

def main():
    print(albion_ascii)
    id_usuario = logar_usuario()
    rows_personagens = menu_personagens(id_usuario)
    id_personagem = selecionar_personagem(rows_personagens)
    while True:
        mover_personagem(id_personagem, criar_cursor())
    
if __name__ == "__main__":
    main()