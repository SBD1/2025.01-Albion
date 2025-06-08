import psycopg2
from psycopg2.extras import RealDictCursor
from simple_term_menu import TerminalMenu
import os
from ascii_art import albion_ascii, encerrar_ascii
import getpass
from limpar_tela import limpar_tela
from operadores.register import register_user
from operadores.login import login
from operadores.visualizar_personagens import visualizar_personagens
from operadores.selecionar_personagem import selecionar_personagem
from operadores.criar_personagem import criar_personagem
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

def main():
    print(albion_ascii)
    id_usuario = logar_usuario()
    rows_personagens = menu_personagens(id_usuario)
    id_personagem = selecionar_personagem(rows_personagens)
    print(f"ID DO PERSONAGEM SELECIONADO: {id_personagem}")
    
if __name__ == "__main__":
    main()