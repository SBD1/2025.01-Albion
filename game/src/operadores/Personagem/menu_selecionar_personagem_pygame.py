from operadores.Menus.estrutura_menu_pygame import MenuPyGame
from operadores.Personagem.visualizar_personagens import visualizar_personagens
from database import criar_cursor
import os
import pygame

def menu_selecionar_personagem_pygame(id_usuario, username):
    """Menu para selecionar personagem implementado em PyGame"""
    menu = MenuPyGame(title="Albion Online - Selecionar Personagem")
    
    # Carregar imagens para o formato com moldura
    caminho_fundo = os.path.join(os.path.dirname(__file__), '../../../assets/fundo.png')
    caminho_moldura = os.path.join(os.path.dirname(__file__), '../../../assets/menu.png')
    
    imagem_fundo = menu.carregar_imagem_fundo(caminho_fundo)
    moldura_rect = pygame.Rect(6, 217, 105, 105)
    moldura_menu = menu.carregar_moldura_menu(caminho_moldura, moldura_rect)
    
    cursor = criar_cursor()
    
    try:
        rows_personagens = visualizar_personagens(id_usuario, cursor)
        
        if not rows_personagens or len(rows_personagens) == 0:
            menu.feedback("Aviso", "Nenhum personagem encontrado.\nCrie um personagem primeiro!", 3000)
            return None
        
        # Preparar lista de personagens para o menu
        opcoes_personagens = []
        for personagem in rows_personagens:
            opcoes_personagens.append(f"{personagem['nome']} ({personagem['especie']}) - Nível {personagem['nivel']}")
        
        opcoes_personagens.append("Voltar")
        
        # Mostrar menu de seleção com moldura
        idx_personagem = menu.set_menu_com_moldura(
            title="SELECIONAR PERSONAGEM",
            options=opcoes_personagens,
            subtitle=f"Usuário: {username}\nEscolha um personagem:",
            imagem_fundo=imagem_fundo,
            moldura=moldura_menu
        )
        
        # Verificar se foi cancelado ou "Voltar"
        if idx_personagem == -1 or idx_personagem == len(opcoes_personagens) - 1:
            return None
        
        # Retornar o personagem selecionado
        personagem_selecionado = rows_personagens[idx_personagem]
        return personagem_selecionado
        
    except Exception as e:
        menu.feedback("Erro", f"Erro ao buscar personagens:\n{str(e)}", 3000)
        return None
