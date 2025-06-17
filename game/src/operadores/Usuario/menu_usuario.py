from game.src.interface import Interface
import sys
import getpass
from game.src.ascii_art import albion_ascii, encerrar_ascii
from game.src.operadores.Usuario.register import register_user
from game.src.operadores.Usuario.login import login
from game.src.database import criar_cursor

def menu_usuario():
    opcoes_login = ["Entrar", "Criar Conta", "Sair"]
    
    while True:
        Interface.limpar_tela()
        print(Interface.CORES['titulo'] + albion_ascii)
        
        # Mostra o menu de opções
        print(Interface.criar_menu("Menu Principal", opcoes_login))
        
        try:
            opcao = int(input()) - 1
            if opcao not in range(len(opcoes_login)):
                Interface.mostrar_erro("Opção inválida!")
                continue
        except ValueError:
            Interface.mostrar_erro("Por favor, digite um número válido!")
            continue

        cursor = criar_cursor()
        
        if opcao == 0:  # Entrar
            Interface.limpar_tela()
            print(Interface.criar_titulo("Login"))
            username = input(Interface.criar_elemento("Digite seu nome de usuário: ", "menu"))
            password = getpass.getpass(Interface.criar_elemento("Digite sua senha: ", "menu"))
            
            Interface.limpar_tela()
            id_usuario = login(username, password, cursor)
            
            if id_usuario:
                Interface.mostrar_sucesso(f"Bem-vindo de volta, {username}!")
                return id_usuario, username
            else:
                Interface.mostrar_erro("Usuário ou senha incorretos!")
                input("Pressione ENTER para continuar...")
            
        elif opcao == 1:  # Criar Conta
            Interface.limpar_tela()
            print(Interface.criar_titulo("Criar Nova Conta"))
            username = input(Interface.criar_elemento("Digite seu nome de usuário: ", "menu"))
            password = getpass.getpass(Interface.criar_elemento("Digite sua senha: ", "menu"))
            
            Interface.limpar_tela()
            try:
                register_user(username, password, cursor)
                Interface.mostrar_sucesso("Conta criada com sucesso!")
                input("Pressione ENTER para continuar...")
            except Exception as e:
                Interface.mostrar_erro(f"Erro ao criar conta: {str(e)}")
                input("Pressione ENTER para continuar...")
            return None, username

        elif opcao == 2:  # Sair
            Interface.limpar_tela()
            print(Interface.CORES['titulo'] + encerrar_ascii)
            Interface.mostrar_info("Obrigado por jogar Albion!")
            sys.exit()
