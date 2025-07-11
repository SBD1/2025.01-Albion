import sys
import os
import pygame
from operadores.Menus.estrutura_menu_pygame import MenuPyGame
from operadores.Usuario.register import register_user
from operadores.Usuario.login import login
from database import criar_cursor

def menu_usuario_pygame():
    menu = MenuPyGame(title="Albion Online")
    
    # Carregar imagens
    caminho_fundo = os.path.join(os.path.dirname(__file__), '../../../assets/fundo.png')
    caminho_moldura = os.path.join(os.path.dirname(__file__), '../../../assets/menu.png')
    
    print(f"DEBUG: Tentando carregar fundo de: {caminho_fundo}")
    print(f"DEBUG: Tentando carregar moldura de: {caminho_moldura}")
    
    imagem_fundo = menu.carregar_imagem_fundo(caminho_fundo)
    moldura_rect = pygame.Rect(6, 217, 105, 105) 
    moldura_menu = menu.carregar_moldura_menu(caminho_moldura, moldura_rect)
    
    print(f"DEBUG: Imagem de fundo carregada: {imagem_fundo is not None}")
    print(f"DEBUG: Moldura carregada: {moldura_menu is not None}")
    
    while True:
        # Opções do menu principal
        opcoes_login = ["Entrar", "Criar Conta", "Sair"]
        
        # Mostrar o menu com fundo e moldura
        opcao = menu.set_menu_com_moldura(
            title="ALBION ONLINE", 
            options=opcoes_login,
            subtitle="Bem-vindo ao mundo de Albion!",
            imagem_fundo=imagem_fundo,
            moldura=moldura_menu
        )
        
        # Processar opções - mantendo lógica idêntica ao original
        cursor = criar_cursor()
        
        if opcao == 0:  # Entrar
            # Mostrar formulário de login
            login_data = menu.set_formulario("LOGIN", "Entrar")
            
            if login_data is None:  # Usuário cancelou
                continue
                
            username, password = login_data
            
            # Validar username
            if len(username) > 30:
                menu.feedback("Erro", "O nome de usuário deve ter no máximo 30 caracteres!", 3000)
                continue
            
            # Tentar fazer login 
            id_usuario = login(username, password, cursor)
            if id_usuario:
                menu.feedback("Sucesso!", f"Bem-vindo de volta, {username}!", 2000)
                return id_usuario, username
            else:
                menu.feedback("Erro", "Nome de usuário ou senha incorretos!", 3000)
                
        elif opcao == 1:  # Criar Conta
            # Mostrar formulário de cadastro
            register_data = menu.set_formulario("CRIAR CONTA", "Cadastrar")
            
            if register_data is None:  # Usuário cancelou
                continue
                
            username, password = register_data
            
            # Validar username
            if len(username) > 30:
                menu.feedback("Erro", "O nome de usuário deve ter no máximo 30 caracteres!", 3000)
                continue
            
            # Tentar criar conta 
            try:
                resultado = register_user(username, password, cursor)
                if resultado is False:
                    # Usuário já existe
                    menu.feedback("Erro", f"O usuário '{username}' já existe!\nEscolha outro nome de usuário.", 3000)
                    continue
                else:
                    menu.feedback("Sucesso!", "Conta criada com sucesso!\nVocê pode fazer login agora.", 3000)
                    # Continua no loop para permitir fazer login
            except Exception as e:
                menu.feedback("Erro", f"Erro ao criar conta:\n{str(e)}", 3000)
                
        elif opcao == 2 or opcao == -1:  # Sair ou ESC
            # Usar feedback customizado para mensagem de despedida
            menu.feedback_despedida("Jogo Finalizado", "Obrigado por jogar Albion!", 2000)
            menu.quit()
            sys.exit()
