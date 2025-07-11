from operadores.Menus.estrutura_menu_pygame import MenuPyGame
from operadores.Personagem.menu_criar_personagem_pygame import menu_criar_personagem_pygame
from operadores.Personagem.menu_selecionar_personagem_pygame import menu_selecionar_personagem_pygame
import os
import pygame

def menu_personagens_pygame(id_usuario, username):
    """Menu principal de personagens - orquestra os submenus de criar e selecionar personagem"""
    menu = MenuPyGame(title="Albion Online - Personagens")
    
    # Carregar imagens para o formato com moldura
    caminho_fundo = os.path.join(os.path.dirname(__file__), '../../../assets/fundo.png')
    caminho_moldura = os.path.join(os.path.dirname(__file__), '../../../assets/menu.png')
    
    imagem_fundo = menu.carregar_imagem_fundo(caminho_fundo)
    moldura_rect = pygame.Rect(6, 217, 105, 105)
    moldura_menu = menu.carregar_moldura_menu(caminho_moldura, moldura_rect)
    
    while True:
        # Opções do menu principal
        opcoes = ["Criar Personagem", "Selecionar Personagem", "Sair"]
        
        # Mostrar o menu com moldura
        opcao = menu.set_menu_com_moldura(
            title="PERSONAGENS",
            options=opcoes,
            subtitle=f"Usuário: {username}",
            imagem_fundo=imagem_fundo,
            moldura=moldura_menu
        )
        
        if opcao == 0:  # Criar Personagem
            sucesso = menu_criar_personagem_pygame(id_usuario, username)

        elif opcao == 1:  # Selecionar Personagem
            personagem_selecionado = menu_selecionar_personagem_pygame(id_usuario, username)
            
            if personagem_selecionado is not None:
                return personagem_selecionado
                
        elif opcao == 2 or opcao == -1:  # Sair ou ESC
            return "voltar"