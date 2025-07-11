from operadores.Menus.estrutura_menu_pygame import MenuPyGame
from operadores.Personagem.criar_personagem import criar_personagem
from database import criar_cursor
import os
import pygame

def menu_criar_personagem_pygame(id_usuario, username):
    """Menu para criar personagem implementado em PyGame - Tela única"""
    menu = MenuPyGame(title="Albion Online - Criar Personagem")
    
    # Carregar imagens para o formato com moldura
    caminho_fundo = os.path.join(os.path.dirname(__file__), '../../../assets/fundo.png')
    caminho_moldura = os.path.join(os.path.dirname(__file__), '../../../assets/menu.png')
    
    imagem_fundo = menu.carregar_imagem_fundo(caminho_fundo)
    moldura_rect = pygame.Rect(6, 217, 105, 105)
    moldura_menu = menu.carregar_moldura_menu(caminho_moldura, moldura_rect)
    
    # Variáveis do formulário
    nome_personagem = ""
    especies = ["Zoiudo", "Draconico", "Espiritualista", "Titan"]
    especie_selecionada = 0
    campo_ativo = 0  # 0 = nome, 1-4 = especies, 5 = botão criar
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu.force_quit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                elif event.key == pygame.K_TAB or event.key == pygame.K_DOWN:
                    campo_ativo = (campo_ativo + 1) % 6  # 6 campos: nome + 4 especies + botão
                elif event.key == pygame.K_UP:
                    campo_ativo = (campo_ativo - 1) % 6
                
                elif event.key == pygame.K_RETURN:
                    if campo_ativo == 0:  # Campo nome
                        campo_ativo = 1  # Vai para primeira espécie
                    elif 1 <= campo_ativo <= 4:  # Especies
                        especie_selecionada = campo_ativo - 1
                        campo_ativo = 5  # Vai para botão criar
                    elif campo_ativo == 5:  # Botão criar
                        if nome_personagem.strip() == "":
                            continue  # Não faz nada se nome vazio
                        # Tentar criar personagem
                        return criar_personagem_agora(id_usuario, nome_personagem.strip(), especies[especie_selecionada], menu)
                
                elif campo_ativo == 0:  # Editando nome
                    if event.key == pygame.K_BACKSPACE:
                        nome_personagem = nome_personagem[:-1]
                    elif len(nome_personagem) < 30 and event.unicode.isprintable():
                        nome_personagem += event.unicode
                
                elif 1 <= campo_ativo <= 4:  # Selecionando espécie
                    if event.key in [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_SPACE]:
                        especie_selecionada = campo_ativo - 1
                        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                
                # Calcular moldura
                moldura_largura = menu.width * 0.4  # Reduzido de 0.45 para 0.4
                moldura_altura = menu.height * 0.8  # Mantém altura
                moldura_x = (menu.width - moldura_largura) // 2
                moldura_y = (menu.height - moldura_altura) // 2
                moldura_rect_calc = pygame.Rect(moldura_x, moldura_y, moldura_largura, moldura_altura)
                
                margin = moldura_largura * 0.15  # Aumentado para campos mais estreitos
                
                # Campo nome
                nome_y = moldura_y + moldura_altura * 0.30
                nome_box = pygame.Rect(moldura_x + margin, nome_y, moldura_largura - 2*margin, 32)  # Reduzido para 32
                if nome_box.collidepoint(mouse_x, mouse_y):
                    campo_ativo = 0
                
                # Botões de espécie
                especies_start_y = moldura_y + moldura_altura * 0.45
                button_height = 30  # Reduzido de 35 para 30
                button_spacing = 36  # Reduzido de 42 para 36
                for i in range(4):
                    button_y = especies_start_y + i * button_spacing
                    button_rect = pygame.Rect(moldura_x + margin, button_y, moldura_largura - 2*margin, button_height)
                    if button_rect.collidepoint(mouse_x, mouse_y):
                        campo_ativo = i + 1
                        especie_selecionada = i
                
                # Botão criar
                criar_button_y = moldura_y + moldura_altura * 0.85
                criar_button = pygame.Rect(moldura_x + moldura_largura*0.2, criar_button_y, moldura_largura*0.6, 38)  # Reduzido altura de 45 para 38
                if criar_button.collidepoint(mouse_x, mouse_y):
                    campo_ativo = 5
                    if nome_personagem.strip():
                        return criar_personagem_agora(id_usuario, nome_personagem.strip(), especies[especie_selecionada], menu)
        
        # Renderização
        menu.set_plano_fundo(imagem_fundo)
        
        # Configurar moldura menor em largura, mesma altura
        moldura_largura = menu.width * 0.4  # Reduzido de 0.45 para 0.4
        moldura_altura = menu.height * 0.8   # Mantém altura
        moldura_x = (menu.width - moldura_largura) // 2
        moldura_y = (menu.height - moldura_altura) // 2
        moldura_rect_render = pygame.Rect(moldura_x, moldura_y, moldura_largura, moldura_altura)
        
        # Desenhar sombra e moldura
        if moldura_menu:
            menu.desenhar_sombra_moldura(moldura_rect_render)
            menu.screen.blit(pygame.transform.scale(moldura_menu, moldura_rect_render.size), moldura_rect_render.topleft)
        
        # Título
        titulo_y = moldura_y + moldura_altura * 0.1
        menu.set_titulo_na_moldura("CRIAR PERSONAGEM", moldura_rect_render.centerx, titulo_y)
        
        # Subtitle com usuário
        subtitle_y = moldura_y + moldura_altura * 0.17
        subtitle_text = f"Usuário: {username}"
        subtitle_surface = menu.renderizar_texto(subtitle_text, menu.font_text, menu.WHITE)
        subtitle_rect = subtitle_surface.get_rect(center=(moldura_rect_render.centerx, subtitle_y))
        menu.screen.blit(subtitle_surface, subtitle_rect)
        
        margin = moldura_largura * 0.15  # Aumentado para campos mais estreitos
        
        # Campo nome
        nome_label_y = moldura_y + moldura_altura * 0.22
        menu.set_texto("Nome do Personagem:", moldura_x + margin, nome_label_y)
        
        nome_y = moldura_y + moldura_altura * 0.25
        nome_box = pygame.Rect(moldura_x + margin, nome_y, moldura_largura - 2*margin, 32)  # Reduzido para 32
        cor_borda = menu.MARROM if campo_ativo == 0 else menu.WHITE
        pygame.draw.rect(menu.screen, menu.WHITE, nome_box)
        pygame.draw.rect(menu.screen, cor_borda, nome_box, 3)
        
        # Texto do nome
        nome_display = nome_personagem + ("|" if campo_ativo == 0 else "")
        if nome_display:
            nome_surface = menu.renderizar_texto(nome_display, menu.font_button, menu.BLACK)
            menu.screen.blit(nome_surface, (nome_box.x + 5, nome_box.y + 5))  # Ajustado para altura menor
        
        # Label espécies
        especies_label_y = moldura_y + moldura_altura * 0.37
        menu.set_texto("Selecione a Espécie:", moldura_x + margin, especies_label_y)
        
        # Botões de espécie
        especies_start_y = moldura_y + moldura_altura * 0.45
        button_height = 30  # Reduzido de 35 para 30
        button_spacing = 36  # Reduzido de 42 para 36
        
        for i, especie in enumerate(especies):
            button_y = especies_start_y + i * button_spacing
            is_selected = (campo_ativo == i + 1) or (especie_selecionada == i and campo_ativo != 0)
            
            button_rect = pygame.Rect(moldura_x + margin, button_y, moldura_largura - 2*margin, button_height)
            
            # Cor do botão
            if is_selected and especie_selecionada == i:
                bg_color = menu.MARROM
                text_color = menu.WHITE
            elif campo_ativo == i + 1:
                bg_color = (200, 200, 200)
                text_color = menu.BLACK
            else:
                bg_color = menu.DARK_GRAY
                text_color = menu.WHITE
            
            pygame.draw.rect(menu.screen, bg_color, button_rect)
            pygame.draw.rect(menu.screen, menu.WHITE, button_rect, 2)
            
            # Texto da espécie
            text_surface = menu.renderizar_texto(especie, menu.font_button, text_color)
            text_rect = text_surface.get_rect(center=button_rect.center)
            menu.screen.blit(text_surface, text_rect)
        
        # Botão criar
        criar_button_y = moldura_y + moldura_altura * 0.85
        criar_button = pygame.Rect(moldura_x + moldura_largura*0.2, criar_button_y, moldura_largura*0.6, 38)  # Reduzido altura de 45 para 38
        
        pode_criar = nome_personagem.strip() != ""
        if campo_ativo == 5:
            bg_color = menu.MARROM if pode_criar else menu.GRAY
        else:
            bg_color = menu.DARK_GRAY if pode_criar else menu.GRAY
            
        text_color = menu.WHITE if pode_criar else menu.DARK_GRAY
        
        pygame.draw.rect(menu.screen, bg_color, criar_button)
        pygame.draw.rect(menu.screen, menu.WHITE, criar_button, 2)
        
        criar_text = menu.renderizar_texto("Criar Personagem", menu.font_button, text_color)
        criar_rect = criar_text.get_rect(center=criar_button.center)
        menu.screen.blit(criar_text, criar_rect)
        
        # Instruções
        instructions = [
            "TAB/↑↓ para navegar entre campos",
            "Enter para confirmar/criar",
            "ESC para cancelar"
        ]
        inst_y = menu.height - (len(instructions) * 25) - 20
        for i, instruction in enumerate(instructions):
            menu.set_texto(instruction, 20, inst_y + i * 25, menu.GRAY)
        
        pygame.display.flip()
        clock.tick(60)

def criar_personagem_agora(id_usuario, nome_personagem, especie_personagem, menu):
    """Função auxiliar para criar o personagem"""
    cursor = criar_cursor()
    try:
        resultado = criar_personagem(id_usuario, nome_personagem, especie_personagem, cursor)
        if resultado:
            menu.feedback(
                "Sucesso!", 
                f"Personagem '{nome_personagem}' ({especie_personagem}) criado com sucesso!",
                3000
            )
            return True
        else:
            menu.feedback("Erro", "Não foi possível criar o personagem. Verifique os dados e tente novamente.", 3000)
            return False
    except Exception as e:
        error_message = str(e)
        
        # Tratar erros específicos com mensagens mais amigáveis
        if "duplicate key value violates unique constraint" in error_message and "nome" in error_message:
            menu.feedback(
                "Erro", 
                f"Já existe um personagem com o nome '{nome_personagem}'.\nEscolha um nome diferente.",
                3000
            )
        elif "personagem_nome_key" in error_message:
            menu.feedback(
                "Erro", 
                f"O nome '{nome_personagem}' já está em uso.\nEscolha um nome diferente.",
                3000
            )
        else:
            menu.feedback("Erro", f"Erro ao criar personagem:\n{str(e)}", 3000)
        return False
