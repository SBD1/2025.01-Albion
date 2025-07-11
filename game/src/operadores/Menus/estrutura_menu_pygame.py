import pygame
import sys
import os
from typing import List, Optional, Tuple

class MenuPyGame:
    _instance = None
    _initialized = False
    
    def __new__(cls, title: str = "Albion Online"):
        if cls._instance is None:
            cls._instance = super(MenuPyGame, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, title: str = "Albion Online"):
        """Inicializa o sistema de menus pygame em tela cheia"""
        if self._initialized:
            return
            
        pygame.init()
        
        # Detectar resolução da tela e usar tela cheia
        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        pygame.display.set_caption(title)
        
        # Configurações de cores
        self.BLACK = (41, 33, 37)
        self.WHITE = (255, 255, 255)
        self.MARROM = (186, 145, 88)
        self.DARK_GREEN = (0, 150, 0)
        self.BLUE = (0, 0, 255)
        self.DARK_BLUE = (0, 0, 150)
        self.GRAY = (128, 128, 128)
        self.DARK_GRAY = (64, 64, 64)
        self.RED = (255, 0, 0)
        
        # Configurar interface responsiva baseada na resolução
        self.scale_factor = self.setup_responsive_ui()
        
        # Estados
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Marcar como inicializado
        self._initialized = True
        
    def renderizar_texto(self, text: str, font: pygame.font.Font, color: Tuple[int, int, int]) -> pygame.Surface:

        return font.render(text, True, color)
    
    def set_botao(self, text: str, x: int, y: int, width: int, height: int, 
                    is_selected: bool = False, is_disabled: bool = False) -> pygame.Rect:

        if is_disabled:
            bg_color = self.GRAY
            text_color = self.DARK_GRAY
        elif is_selected:
            bg_color = self.MARROM
            text_color = self.WHITE
        else:
            bg_color = self.DARK_GRAY
            text_color = self.WHITE
            
        # Desenha o botão
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, bg_color, button_rect)
        pygame.draw.rect(self.screen, self.WHITE, button_rect, 2)
        
        # Desenha o texto
        text_surface = self.renderizar_texto(text, self.font_button, text_color)
        text_rect = text_surface.get_rect(center=button_rect.center)
        self.screen.blit(text_surface, text_rect)
        
        return button_rect
    
    def set_titulo(self, title: str, y: int = 50):
        title_surface = self.renderizar_texto(title, self.font_title, self.MARROM)
        title_rect = title_surface.get_rect(center=(self.width // 2, y))
        self.screen.blit(title_surface, title_rect)
        
    def set_texto(self, text: str, x: int, y: int, color: Tuple[int, int, int] = None):
        if color is None:
            color = self.WHITE
        text_surface = self.renderizar_texto(text, self.font_text, color)
        self.screen.blit(text_surface, (x, y))
    
    def set_titulo_na_moldura(self, title: str, center_x: int, y: int):
        title_surface = self.renderizar_texto(title, self.font_title, self.MARROM)
        title_rect = title_surface.get_rect(center=(center_x, y))
        self.screen.blit(title_surface, title_rect)
    
    def desenhar_sombra_moldura(self, moldura_rect: pygame.Rect, offset: int = 8, alpha: int = 100):
        sombra_rect = moldura_rect.copy()
        sombra_rect.x += offset
        sombra_rect.y += offset
        
        # Criar superfície com transparência
        sombra_surface = pygame.Surface(sombra_rect.size, pygame.SRCALPHA)
        sombra_surface.fill((0, 0, 0, alpha))
        self.screen.blit(sombra_surface, sombra_rect)
        
    def set_menu(self, title: str, options: List[str], subtitle: str = "") -> int:
        """
        Mostra um menu com opções e retorna o índice da opção selecionada
        Retorna -1 se o usuário fechou a janela
        """
        selected = 0
        scroll_offset = 0
        clock = pygame.time.Clock()
        
        # Calcular quantos itens cabem na tela
        start_y = 150
        if subtitle:
            # Calcular espaço necessário para o subtítulo baseado no número de linhas
            subtitle_lines = subtitle.split('\n')
            line_height = 25  # Altura por linha de subtítulo
            subtitle_height = len(subtitle_lines) * line_height
            start_y = 120 + subtitle_height + 40  # Título + subtítulo + margem
        
        spacing = self.get_adaptive_spacing()
        available_height = self.height - start_y - 120  # Reservar espaço para instruções
        items_per_page = max(3, available_height // spacing)  # Mínimo 3 itens visíveis
        
        while True:
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and selected > 0:
                        selected -= 1
                        # Ajustar scroll se necessário
                        if selected < scroll_offset:
                            scroll_offset = selected
                    elif event.key == pygame.K_DOWN and selected < len(options) - 1:
                        selected += 1
                        # Ajustar scroll se necessário
                        if selected >= scroll_offset + items_per_page:
                            scroll_offset = selected - items_per_page + 1
                    elif event.key == pygame.K_PAGEUP:
                        selected = max(0, selected - items_per_page)
                        scroll_offset = max(0, selected - items_per_page // 2)
                    elif event.key == pygame.K_PAGEDOWN:
                        selected = min(len(options) - 1, selected + items_per_page)
                        if selected >= scroll_offset + items_per_page:
                            scroll_offset = selected - items_per_page + 1
                    elif event.key == pygame.K_HOME:
                        selected = 0
                        scroll_offset = 0
                    elif event.key == pygame.K_END:
                        selected = len(options) - 1
                        scroll_offset = max(0, len(options) - items_per_page)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return selected
                    elif event.key == pygame.K_ESCAPE:
                        return -1
                        
                elif event.type == pygame.MOUSEMOTION:
                    mouse_y = event.pos[1]
                    spacing = self.get_adaptive_spacing()
                    button_height = self.get_adaptive_button_size()[1]
                    # Calcular qual opção está sendo apontada (relativa ao scroll)
                    for i in range(min(len(options) - scroll_offset, items_per_page)):
                        button_y = start_y + i * spacing
                        if button_y <= mouse_y <= button_y + button_height:
                            new_selected = scroll_offset + i
                            if 0 <= new_selected < len(options):
                                selected = new_selected
                            break
                            
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clique esquerdo
                        mouse_y = event.pos[1]
                        spacing = self.get_adaptive_spacing()
                        button_height = self.get_adaptive_button_size()[1]
                        for i in range(min(len(options) - scroll_offset, items_per_page)):
                            button_y = start_y + i * spacing
                            if button_y <= mouse_y <= button_y + button_height:
                                clicked_option = scroll_offset + i
                                if 0 <= clicked_option < len(options):
                                    return clicked_option
                    elif event.button == 4:  # Scroll do mouse para cima
                        if scroll_offset > 0:
                            scroll_offset -= 1
                            if selected >= scroll_offset + items_per_page:
                                selected = scroll_offset + items_per_page - 1
                    elif event.button == 5:  # Scroll do mouse para baixo
                        if scroll_offset < len(options) - items_per_page:
                            scroll_offset += 1
                            if selected < scroll_offset:
                                selected = scroll_offset
            
            # Renderização
            self.screen.fill(self.BLACK)
            
            # Título
            self.set_titulo(title)
            
            # Subtítulo se houver (suporta múltiplas linhas)
            if subtitle:
                subtitle_lines = subtitle.split('\n')
                for i, line in enumerate(subtitle_lines):
                    subtitle_surface = self.renderizar_texto(line, self.font_text, self.WHITE)
                    subtitle_rect = subtitle_surface.get_rect(center=(self.width // 2, 120 + i * 25))
                    self.screen.blit(subtitle_surface, subtitle_rect)
            
            # Opções do menu (apenas as visíveis)
            button_width, button_height = self.get_adaptive_button_size()
            button_x = (self.width - button_width) // 2
            spacing = self.get_adaptive_spacing()
            
            visible_options = options[scroll_offset:scroll_offset + items_per_page]
            for i, option in enumerate(visible_options):
                actual_index = scroll_offset + i
                button_y = start_y + i * spacing
                is_selected = (actual_index == selected)
                
                # Truncar texto muito longo
                display_text = option
                max_chars = max(50, int(self.width / 25))  # Adaptar baseado na largura
                if len(display_text) > max_chars:
                    display_text = display_text[:max_chars-3] + "..."
                
                self.set_botao(display_text, button_x, button_y, button_width, button_height, is_selected)
            
            # Indicadores de scroll
            if len(options) > items_per_page:
                spacing = self.get_adaptive_spacing()
                # Indicador de que há mais itens acima
                if scroll_offset > 0:
                    self.set_texto("▲ Mais opções acima", self.width - 200, start_y - 25, self.MARROM)
                
                # Indicador de que há mais itens abaixo
                if scroll_offset + items_per_page < len(options):
                    self.set_texto("▼ Mais opções abaixo", self.width - 200, start_y + items_per_page * spacing, self.MARROM)
                
                # Contador de página
                current_page = (scroll_offset // items_per_page) + 1
                total_pages = ((len(options) - 1) // items_per_page) + 1
                page_info = f"Página {current_page}/{total_pages} ({len(options)} itens)"
                self.set_texto(page_info, 10, start_y - 25, self.GRAY)
            
            # Instruções (adaptadas para scroll)
            instructions = [
                "↑/↓ ou mouse para navegar",
                "PgUp/PgDown para páginas",
                "Home/End para início/fim",
                "Enter/Espaço/Clique para selecionar",
                "ESC para voltar"
            ]
            if len(options) > items_per_page:
                instructions.insert(2, "Scroll do mouse para rolar")
            
            for i, instruction in enumerate(instructions):
                self.set_texto(instruction, 10, self.height - 120 + i * 20, self.GRAY)
            
            pygame.display.flip()
            clock.tick(60)
    
    def feedback(self, title: str, message: str, duration: int = 3000, large_text: bool = False):
        # Preparar superfícies de texto
        title_surf = self.font_title.render(title, True, self.MARROM)
        lines = message.split('\n')
        msg_surfs = [self.font_text.render(line, True, self.WHITE) for line in lines]
        # Calcular largura e altura da moldura
        padding_x = 20
        padding_y = 20
        max_text_width = max(title_surf.get_width(), *(surf.get_width() for surf in msg_surfs))
        total_text_height = title_surf.get_height() + sum(surf.get_height() for surf in msg_surfs) + (len(msg_surfs) * 10)
        frame_width = max_text_width + padding_x * 2
        frame_height = total_text_height + padding_y * 2
        # Centralizar moldura
        x = (self.width - frame_width) // 2
        y = (self.height - frame_height) // 2
        frame_rect = pygame.Rect(x, y, frame_width, frame_height)
        # Loop de exibição
        start_time = pygame.time.get_ticks()
        clock = pygame.time.Clock()
        while pygame.time.get_ticks() - start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); sys.exit()
            # Desenhar fundo escuro semitransparente
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            self.screen.blit(overlay, (0, 0))
            # Desenhar moldura
            pygame.draw.rect(self.screen, self.DARK_GRAY, frame_rect)
            pygame.draw.rect(self.screen, self.MARROM, frame_rect, 3)
            # Desenhar título
            title_x = x + (frame_width - title_surf.get_width()) // 2
            title_y = y + padding_y
            self.screen.blit(title_surf, (title_x, title_y))
            # Desenhar mensagens centralizadas
            text_y = title_y + title_surf.get_height() + 10
            for surf in msg_surfs:
                # Centralizar horizontalmente dentro da moldura
                text_x = x + (frame_width - surf.get_width()) // 2
                self.screen.blit(surf, (text_x, text_y))
                text_y += surf.get_height() + 10
            pygame.display.flip()
            clock.tick(60)
    
    def feedback_despedida(self, title: str, message: str, duration: int = 3000):
        """Mostra uma mensagem de despedida especial com moldura ajustada"""
        import os
        start_time = pygame.time.get_ticks()
        clock = pygame.time.Clock()
        
        # Carregar recursos para consistência visual
        caminho_fundo = os.path.join(os.path.dirname(__file__), '../../../assets/fundo.png')
        caminho_moldura = os.path.join(os.path.dirname(__file__), '../../../assets/menu.png')
        imagem_fundo = self.carregar_imagem_fundo(caminho_fundo)
        
        # Usar a mesma configuração de moldura
        rect_moldura_sprite = pygame.Rect(6, 217, 105, 105)
        moldura = self.carregar_moldura_menu(caminho_moldura, rect_moldura_sprite)

        while pygame.time.get_ticks() - start_time < duration:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    return  # Sair mais cedo se usuário pressionar algo
            
            # Renderização
            self.set_plano_fundo(imagem_fundo)
            
            # Configurar moldura adequada para despedida
            if moldura:
                moldura_largura = min(self.width * 0.5, 600)  # Aumentado para comportar melhor o texto
                moldura_altura = min(self.height * 0.35, 300)  # Aumentado para comportar melhor o texto
                moldura_x = (self.width - moldura_largura) // 2
                moldura_y = (self.height - moldura_altura) // 2
                moldura_rect = pygame.Rect(moldura_x, moldura_y, moldura_largura, moldura_altura)
                
                # Desenhar sombra e moldura
                self.desenhar_sombra_moldura(moldura_rect)
                self.screen.blit(pygame.transform.scale(moldura, moldura_rect.size), moldura_rect.topleft)
                
                # Título dentro da moldura (usando font_button para não ficar muito grande)
                titulo_y = moldura_rect.y + int(moldura_altura * 0.2)
                self.set_titulo_na_moldura(title, moldura_rect.centerx, titulo_y)
                
                # Mensagem dentro da moldura (usando font_button em vez de font_title)
                lines = message.split('\n')
                line_height = self.font_button.get_height()
                total_text_height = len(lines) * line_height
                start_msg_y = moldura_rect.centery - total_text_height // 2 + 10
                
                for i, line in enumerate(lines):
                    message_surface = self.renderizar_texto(line, self.font_button, self.WHITE)
                    message_rect = message_surface.get_rect(center=(moldura_rect.centerx, start_msg_y + i * line_height))
                    self.screen.blit(message_surface, message_rect)
                
                # Instruções dentro da moldura
                instruction_text = ""
                instruction_surface = self.renderizar_texto(instruction_text, self.font_small, self.GRAY)
                instruction_rect = instruction_surface.get_rect(center=(moldura_rect.centerx, moldura_rect.bottom - 25))
                self.screen.blit(instruction_surface, instruction_rect)
            else:
                # Fallback sem moldura
                self.screen.fill(self.BLACK)
                self.set_titulo(title)
                
                lines = message.split('\n')
                start_y = 200
                for i, line in enumerate(lines):
                    text_surface = self.renderizar_texto(line, self.font_button, self.WHITE)
                    text_rect = text_surface.get_rect(center=(self.width // 2, start_y + i * 35))
                    self.screen.blit(text_surface, text_rect)
            
            pygame.display.flip()
            clock.tick(60)
    
    def set_formulario(self, title: str, button_text: str = "Confirmar") -> Optional[Tuple[str, str]]:
        """
        Mostra um formulário de usuário com campos de username e senha
        Retorna uma tupla (username, password) ou None se cancelado
        """
        username = ""
        password = ""
        active_field = 0  # 0 = username, 1 = password, 2 = botão login
        clock = pygame.time.Clock()
        
        # Carregar recursos visuais para consistência
        import os
        caminho_fundo = os.path.join(os.path.dirname(__file__), '../../../assets/fundo.png')
        caminho_moldura = os.path.join(os.path.dirname(__file__), '../../../assets/menu.png')
        imagem_fundo = self.carregar_imagem_fundo(caminho_fundo)
        rect_moldura_sprite = pygame.Rect(6, 217, 105, 105)
        moldura = self.carregar_moldura_menu(caminho_moldura, rect_moldura_sprite)
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.force_quit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        active_field = (active_field + 1) % 3
                    elif event.key == pygame.K_UP and active_field > 0:
                        active_field -= 1
                    elif event.key == pygame.K_DOWN and active_field < 2:
                        active_field += 1
                    elif event.key == pygame.K_RETURN:
                        if active_field == 2:  # Botão confirmar
                            if username.strip() and password.strip():
                                return (username.strip(), password.strip())
                            else:
                                # Mostrar erro se campos vazios
                                continue
                        else:
                            active_field = (active_field + 1) % 3
                    elif event.key == pygame.K_ESCAPE:
                        return None
                    elif active_field == 0:  # Campo username
                        if event.key == pygame.K_BACKSPACE:
                            username = username[:-1]
                        elif len(username) < 30 and event.unicode.isprintable():
                            username += event.unicode
                    elif active_field == 1:  # Campo password
                        if event.key == pygame.K_BACKSPACE:
                            password = password[:-1]
                        elif len(password) < 50 and event.unicode.isprintable():
                            password += event.unicode
                            
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = event.pos
                    
                    # Calcular moldura e campos
                    moldura_largura = self.width * 0.5
                    moldura_altura = self.height * 0.6
                    moldura_x = (self.width - moldura_largura) // 2
                    moldura_y = (self.height - moldura_altura) // 2
                    moldura_rect = pygame.Rect(moldura_x, moldura_y, moldura_largura, moldura_altura)
                    
                    # Calcular campos dentro da moldura
                    margin = moldura_largura * 0.1
                    input_width = moldura_largura - (2 * margin)
                    input_height = max(40, int(moldura_altura * 0.08))
                    button_width = moldura_largura * 0.4
                    button_height = max(50, int(moldura_altura * 0.1))
                    
                    # Posições dos campos
                    username_box = pygame.Rect(moldura_x + margin, moldura_y + moldura_altura * 0.36, input_width, input_height)
                    password_box = pygame.Rect(moldura_x + margin, moldura_y + moldura_altura * 0.56, input_width, input_height)
                    confirm_button = pygame.Rect(moldura_x + (moldura_largura - button_width) // 2, moldura_y + moldura_altura * 0.72, button_width, button_height)
                    
                    if username_box.collidepoint(mouse_x, mouse_y):
                        active_field = 0
                    elif password_box.collidepoint(mouse_x, mouse_y):
                        active_field = 1
                    elif confirm_button.collidepoint(mouse_x, mouse_y):
                        if username.strip() and password.strip():
                            return (username.strip(), password.strip())
            
            # Renderização
            # 1. Desenhar fundo
            if imagem_fundo:
                self.screen.blit(imagem_fundo, (0, 0))
            else:
                self.screen.fill(self.BLACK)
            
            # 2. Calcular moldura
            moldura_largura = self.width * 0.5
            moldura_altura = self.height * 0.6
            moldura_x = (self.width - moldura_largura) // 2
            moldura_y = (self.height - moldura_altura) // 2
            moldura_rect = pygame.Rect(moldura_x, moldura_y, moldura_largura, moldura_altura)
            
            # 3. Desenhar sombra e moldura
            if moldura:
                self.desenhar_sombra_moldura(moldura_rect)
                self.screen.blit(pygame.transform.scale(moldura, moldura_rect.size), moldura_rect.topleft)
            
            # 4. Título dentro da moldura
            titulo_y = moldura_y + moldura_altura * 0.15
            self.set_titulo_na_moldura(title, moldura_rect.centerx, titulo_y)
            
            # 5. Calcular campos dentro da moldura
            margin = moldura_largura * 0.1
            input_width = moldura_largura - (2 * margin)
            input_height = max(40, int(moldura_altura * 0.12))
            button_width = moldura_largura * 0.4
            button_height = max(50, int(moldura_altura * 0.1))
            
            # 6. Label e campo username
            username_label_y = moldura_y + moldura_altura * 0.32
            self.set_texto("Nome de usuário:", moldura_x + margin, username_label_y)
            
            username_box = pygame.Rect(moldura_x + margin, moldura_y + moldura_altura * 0.36, input_width, input_height)
            box_color = self.MARROM if active_field == 0 else self.WHITE
            pygame.draw.rect(self.screen, self.WHITE, username_box)
            pygame.draw.rect(self.screen, box_color, username_box, 2)
            
            # Texto do username
            username_display = username + ("|" if active_field == 0 else "")
            text_surface = self.renderizar_texto(username_display, self.font_button, self.BLACK)
            self.screen.blit(text_surface, (username_box.x + 5, username_box.y + input_height // 4))
            
            # 7. Label e campo password
            password_label_y = moldura_y + moldura_altura * 0.52
            self.set_texto("Senha:", moldura_x + margin, password_label_y)
            
            password_box = pygame.Rect(moldura_x + margin, moldura_y + moldura_altura * 0.56, input_width, input_height)
            box_color = self.MARROM if active_field == 1 else self.WHITE
            pygame.draw.rect(self.screen, self.WHITE, password_box)
            pygame.draw.rect(self.screen, box_color, password_box, 2)
            
            # Texto da senha (asteriscos)
            password_display = "*" * len(password) + ("|" if active_field == 1 else "")
            text_surface = self.renderizar_texto(password_display, self.font_button, self.BLACK)
            self.screen.blit(text_surface, (password_box.x + 5, password_box.y + input_height // 4))
            
            # 8. Botão de confirmação
            confirm_button = pygame.Rect(moldura_x + (moldura_largura - button_width) // 2, moldura_y + moldura_altura * 0.72, button_width, button_height)
            button_selected = active_field == 2
            can_confirm = username.strip() != "" and password.strip() != ""
            self.set_botao(button_text, confirm_button.x, confirm_button.y, 
                           confirm_button.width, confirm_button.height, 
                           button_selected, not can_confirm)
            
            # 9. Mensagem de erro se campos vazios (dentro da moldura)
            if active_field == 2 and (not username.strip() or not password.strip()):
                error_msg = "Preencha todos os campos!"
                error_surface = self.renderizar_texto(error_msg, self.font_text, self.RED)
                error_rect = error_surface.get_rect(center=(moldura_rect.centerx, moldura_y + moldura_altura * 0.82))
                self.screen.blit(error_surface, error_rect)
            
            # 10. Instruções (fora da moldura, na parte inferior)
            instructions = [
                "TAB/↑↓ para navegar entre campos",
                "Enter para confirmar",
                "ESC para cancelar"
            ]
            inst_y = self.height - (len(instructions) * 25) - 20
            for i, instruction in enumerate(instructions):
                self.set_texto(instruction, 20, inst_y + i * 25, self.GRAY)
            
            pygame.display.flip()
            clock.tick(60)
        
        return None

    def quit(self):
        """Limpa a tela sem fechar o pygame"""
        if hasattr(self, 'screen'):
            self.screen.fill(self.BLACK)
            pygame.display.flip()
    
    def force_quit(self):
        """Força o fechamento completo do pygame (apenas ao sair do jogo)"""
        pygame.quit()
        sys.exit()
    
    def setup_responsive_ui(self):
        """Configura a interface baseada na resolução da tela"""
        # Determinar escala baseada na largura da tela
        # 1920 como referência para escala 1.0
        scale_factor = self.width / 1920.0
        scale_factor = max(0.7, min(scale_factor, 2.0))  # Limitar entre 0.7 e 2.0
        
        # Ajustar tamanhos de fonte baseado na escala
        base_title_size = int(72 * scale_factor)
        base_button_size = int(42 * scale_factor)
        base_text_size = int(32 * scale_factor)
        base_small_size = int(28 * scale_factor)
        
        # Recriar fontes com novos tamanhos
        self.font_title = pygame.font.Font(None, base_title_size)
        self.font_button = pygame.font.Font(None, base_button_size)
        self.font_text = pygame.font.Font(None, base_text_size)
        self.font_small = pygame.font.Font(None, base_small_size)
        
        # Ajustar itens por página baseado na altura
        self.items_per_page = max(3, (self.height - 350) // max(50, int(60 * scale_factor)))
        
        return scale_factor
    
    def get_adaptive_button_size(self):
        """Retorna tamanho adaptativo para botões baseado na resolução"""
        base_width = min(800, self.width - 200)
        base_height = max(50, int(self.height * 0.04))  # 4% da altura da tela
        return base_width, base_height
    
    def get_adaptive_spacing(self):
        """Retorna espaçamento adaptativo baseado na resolução"""
        base_spacing = max(50, int(self.height * 0.05))  # 5% da altura da tela
        return base_spacing
    
    def show_scrollable_text(self, title: str, content: str, back_button_text: str = "Voltar") -> int:
        """
        Mostra texto longo com capacidade de scroll vertical
        Ideal para descrições, atributos detalhados, etc.
        """
        selected = 0
        scroll_offset = 0
        clock = pygame.time.Clock()
        
        # Dividir o conteúdo em linhas
        lines = content.split('\n')
        
        # Calcular quantas linhas cabem na tela
        start_y = 150
        line_height = max(25, int(self.height * 0.025))
        available_height = self.height - start_y - 120  # Reservar espaço para instruções
        lines_per_page = max(5, available_height // line_height)
        
        # Opções do menu (só tem o botão voltar)
        options = [back_button_text]
        
        while True:
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and scroll_offset > 0:
                        scroll_offset -= 1
                    elif event.key == pygame.K_DOWN and scroll_offset < len(lines) - lines_per_page:
                        scroll_offset += 1
                    elif event.key == pygame.K_PAGEUP:
                        scroll_offset = max(0, scroll_offset - lines_per_page)
                    elif event.key == pygame.K_PAGEDOWN:
                        scroll_offset = min(len(lines) - lines_per_page, scroll_offset + lines_per_page)
                    elif event.key == pygame.K_HOME:
                        scroll_offset = 0
                    elif event.key == pygame.K_END:
                        scroll_offset = max(0, len(lines) - lines_per_page)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                        return 0  # Sempre retorna 0 (voltar)
                        
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clique esquerdo
                        # Verificar se clicou no botão voltar (na parte inferior)
                        button_y = self.height - 100
                        mouse_y = event.pos[1]
                        if button_y <= mouse_y <= button_y + 50:
                            return 0
                    elif event.button == 4:  # Scroll do mouse para cima
                        if scroll_offset > 0:
                            scroll_offset -= 3
                    elif event.button == 5:  # Scroll do mouse para baixo
                        if scroll_offset < len(lines) - lines_per_page:
                            scroll_offset += 3
            
            # Renderização
            self.screen.fill(self.BLACK)
            
            # Título
            self.set_titulo(title)
            
            # Conteúdo scrollável
            visible_lines = lines[scroll_offset:scroll_offset + lines_per_page]
            for i, line in enumerate(visible_lines):
                line_y = start_y + i * line_height
                # Usar fonte menor para textos longos
                text_surface = self.renderizar_texto(line, self.font_small, self.WHITE)
                self.screen.blit(text_surface, (50, line_y))
            
            # Indicadores de scroll
            if len(lines) > lines_per_page:
                # Indicador de que há mais texto acima
                if scroll_offset > 0:
                    self.set_texto("▲ Mais texto acima", self.width - 200, start_y - 25, self.MARROM)
                
                # Indicador de que há mais texto abaixo
                if scroll_offset + lines_per_page < len(lines):
                    self.set_texto("▼ Mais texto abaixo", self.width - 200, start_y + lines_per_page * line_height, self.MARROM)
                
                # Contador de posição
                current_line = scroll_offset + 1
                end_line = min(scroll_offset + lines_per_page, len(lines))
                position_info = f"Linhas {current_line}-{end_line} de {len(lines)}"
                self.set_texto(position_info, 50, start_y - 25, self.GRAY)
            
            # Botão voltar na parte inferior
            button_width, button_height = self.get_adaptive_button_size()
            button_x = (self.width - button_width) // 2
            button_y = self.height - 100
            self.set_botao(back_button_text, button_x, button_y, button_width, button_height, True)
            
            # Instruções
            instructions = [
                "↑/↓ ou scroll do mouse para rolar",
                "PgUp/PgDown para páginas",
                "Home/End para início/fim",
                "Enter/Espaço/ESC/Clique para voltar"
            ]
            
            for i, instruction in enumerate(instructions):
                self.set_texto(instruction, 10, self.height - 160 + i * 20, self.GRAY)
            
            pygame.display.flip()
            clock.tick(60)
    
    def carregar_imagem_fundo(self, caminho_imagem: str):
        """Carrega e redimensiona a imagem de fundo para a resolução da tela"""
        try:
            import os
            if not os.path.exists(caminho_imagem):
                print(f"Aviso: Imagem de fundo não encontrada: {caminho_imagem}")
                return None
            
            imagem = pygame.image.load(caminho_imagem).convert()
            # Redimensionar para a resolução da tela mantendo proporção
            imagem_redimensionada = pygame.transform.scale(imagem, (self.width, self.height))
            return imagem_redimensionada
        except Exception as e:
            print(f"Erro ao carregar imagem de fundo: {e}")
            return None
    
    def carregar_moldura_menu(self, caminho_imagem: str, rect_moldura: pygame.Rect):
        """Carrega a moldura do menu a partir de coordenadas específicas"""
        try:
            import os
            if not os.path.exists(caminho_imagem):
                print(f"Aviso: Imagem de moldura não encontrada: {caminho_imagem}")
                return None
            
            sprite_sheet = pygame.image.load(caminho_imagem).convert_alpha()
            moldura = pygame.Surface((rect_moldura.width, rect_moldura.height), pygame.SRCALPHA)
            moldura.blit(sprite_sheet, (0, 0), rect_moldura)
            return moldura
        except Exception as e:
            print(f"Erro ao carregar moldura do menu: {e}")
            return None
    
    def set_plano_fundo(self, imagem_fundo: pygame.Surface):
        """Desenha a imagem de fundo ocupando toda a tela."""
        if imagem_fundo:
            self.screen.blit(imagem_fundo, (0, 0))
    
    def set_menu_com_moldura(self, title: str, options: List[str], subtitle: str = "", 
                            imagem_fundo=None, moldura=None) -> int:
        """
        Versão especial do menu com fundo e moldura personalizados
        """
        selected = 0
        scroll_offset = 0
        clock = pygame.time.Clock()
        
        # Variáveis que serão calculadas dinamicamente baseadas na moldura
        start_y = 250
        spacing = self.get_adaptive_spacing()
        button_x = 0
        button_width = 0
        button_height = 0
        items_per_page = max(3, (self.height - 300) // spacing)
        titulo_y = 100
        subtitle_y = 150
        
        while True:
            # Calcular moldura primeiro para definir layout
            moldura_rect = None
            if moldura:
                # Tamanho da moldura proporcional à tela
                moldura_largura = min(self.width * 0.7, 800)
                moldura_altura = min(self.height * 0.7, 600)
                moldura_x = (self.width - moldura_largura) // 2
                moldura_y = (self.height - moldura_altura) // 2
                moldura_rect = pygame.Rect(moldura_x, moldura_y, moldura_largura, moldura_altura)
                
                # Ajustar variáveis baseadas na moldura com margem interna apropriada
                margin = int(moldura_largura * 0.10)  # 10% da largura como margem
                
                # Ajustar posições para ficar dentro da moldura
                titulo_y = moldura_rect.y + int(moldura_altura * 0.15)  # 15% da altura
                subtitle_y = moldura_rect.y + int(moldura_altura * 0.25)  # 25% da altura
                
                # Dimensões dos botões ajustadas à moldura
                button_width = moldura_rect.width - (2 * margin)
                button_height = max(35, int(moldura_altura * 0.10))  # 8% da altura da moldura
                button_x = moldura_rect.x + margin
                start_y = moldura_rect.y + int(moldura_altura * 0.35)  # 35% da altura
                
                # Calcular espaço disponível para botões
                available_height = moldura_rect.height - int(moldura_altura * 0.45)  # Reservar 45% para título/subtítulo
                spacing = max(button_height + 8, int(available_height / max(1, len(options))))
                items_per_page = max(1, available_height // spacing)
            else:
                # Layout normal sem moldura
                button_width, button_height = self.get_adaptive_button_size()
                button_x = (self.width - button_width) // 2
                start_y = 250 if subtitle else 200
                titulo_y = 100
                subtitle_y = 150
                if subtitle:
                    start_y += 50
            
            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and selected > 0:
                        selected -= 1
                        if selected < scroll_offset:
                            scroll_offset = selected
                    elif event.key == pygame.K_DOWN and selected < len(options) - 1:
                        selected += 1
                        if selected >= scroll_offset + items_per_page:
                            scroll_offset = selected - items_per_page + 1
                    elif event.key == pygame.K_PAGEUP:
                        selected = max(0, selected - items_per_page)
                        scroll_offset = max(0, selected - items_per_page // 2)
                    elif event.key == pygame.K_PAGEDOWN:
                        selected = min(len(options) - 1, selected + items_per_page)
                        if selected >= scroll_offset + items_per_page:
                            scroll_offset = selected - items_per_page + 1
                    elif event.key == pygame.K_HOME:
                        selected = 0
                        scroll_offset = 0
                    elif event.key == pygame.K_END:
                        selected = len(options) - 1
                        scroll_offset = max(0, len(options) - items_per_page)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return selected
                    elif event.key == pygame.K_ESCAPE:
                        return -1
                        
                elif event.type == pygame.MOUSEMOTION:
                    mouse_y = event.pos[1]
                    # Usar as variáveis calculadas baseadas na moldura
                    for i in range(min(len(options) - scroll_offset, items_per_page)):
                        button_y = start_y + i * spacing
                        if button_y <= mouse_y <= button_y + button_height:
                            new_selected = scroll_offset + i
                            if 0 <= new_selected < len(options):
                                selected = new_selected
                            break
                            
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_y = event.pos[1]
                        # Usar as variáveis calculadas baseadas na moldura
                        for i in range(min(len(options) - scroll_offset, items_per_page)):
                            button_y = start_y + i * spacing
                            if button_y <= mouse_y <= button_y + button_height:
                                clicked_option = scroll_offset + i
                                if 0 <= clicked_option < len(options):
                                    return clicked_option
                    elif event.button == 4:
                        if scroll_offset > 0:
                            scroll_offset -= 1
                            if selected >= scroll_offset + items_per_page:
                                selected = scroll_offset + items_per_page - 1
                    elif event.button == 5:
                        if scroll_offset < len(options) - items_per_page:
                            scroll_offset += 1
                            if selected < scroll_offset:
                                selected = scroll_offset
            
            # Renderização
            # 1. Desenhar fundo
            self.set_plano_fundo(imagem_fundo)
            
            # 2. Desenhar sombra da moldura antes da moldura (para efeito de flutuação)
            if moldura and moldura_rect:
                self.desenhar_sombra_moldura(moldura_rect)
            
            # 3. Desenhar moldura se houver
            if moldura and moldura_rect:
                self.screen.blit(pygame.transform.scale(moldura, (moldura_rect.width, moldura_rect.height)), 
                               (moldura_rect.x, moldura_rect.y))
            
            # 4. Título (posicionado dentro da moldura se existir)
            if moldura_rect:
                self.set_titulo_na_moldura(title, moldura_rect.centerx, titulo_y)
            else:
                self.set_titulo(title, titulo_y)
            
            # 5. Subtítulo se houver (posicionado dentro da moldura se existir)
            if subtitle:
                subtitle_lines = subtitle.split('\n')
                for i, line in enumerate(subtitle_lines):
                    subtitle_surface = self.renderizar_texto(line, self.font_text, self.WHITE)
                    if moldura_rect:
                        subtitle_rect = subtitle_surface.get_rect(center=(moldura_rect.centerx, subtitle_y + i * 25))
                    else:
                        subtitle_rect = subtitle_surface.get_rect(center=(self.width // 2, subtitle_y + i * 25))
                    self.screen.blit(subtitle_surface, subtitle_rect)
            
            # 5. Opções do menu (usando variáveis já calculadas)
            visible_options = options[scroll_offset:scroll_offset + items_per_page]
            for i, option in enumerate(visible_options):
                actual_index = scroll_offset + i
                button_y = start_y + i * spacing
                is_selected = (actual_index == selected)
                
                display_text = option
                max_chars = max(15, int(button_width / 12))
                if len(display_text) > max_chars:
                    display_text = display_text[:max_chars-3] + "..."
                
                self.set_botao(display_text, button_x, button_y, button_width, button_height, is_selected)
            
            # 6. Indicadores de scroll (posicionados dentro da moldura se existir)
            if len(options) > items_per_page:
                if moldura_rect:
                    # Indicadores mais discretos e posicionados dentro da moldura
                    if scroll_offset > 0:
                        self.set_texto("▲", moldura_rect.right - 25, start_y - 5, self.MARROM)
                    
                    if scroll_offset + items_per_page < len(options):
                        last_button_y = start_y + (min(items_per_page, len(options) - scroll_offset) - 1) * spacing
                        self.set_texto("▼", moldura_rect.right - 25, last_button_y + button_height - 15, self.MARROM)
                    
                    # Informação de página mais sutil
                    current_page = (scroll_offset // items_per_page) + 1
                    total_pages = ((len(options) - 1) // items_per_page) + 1
                    page_info = f"{current_page}/{total_pages}"
                    page_surface = self.renderizar_texto(page_info, self.font_small, self.GRAY)
                    page_rect = page_surface.get_rect(center=(moldura_rect.centerx, moldura_rect.bottom - 15))
                    self.screen.blit(page_surface, page_rect)
                else:
                    # Comportamento original para quando não há moldura
                    if scroll_offset > 0:
                        self.set_texto("▲ Mais opções acima", self.width - 200, start_y - 25, self.MARROM)
                    
                    if scroll_offset + items_per_page < len(options):
                        self.set_texto("▼ Mais opções abaixo", self.width - 200, start_y + items_per_page * spacing, self.MARROM)
                    
                    current_page = (scroll_offset // items_per_page) + 1
                    total_pages = ((len(options) - 1) // items_per_page) + 1
                    page_info = f"Página {current_page}/{total_pages} ({len(options)} itens)"
                    self.set_texto(page_info, 10, start_y - 25, self.GRAY)
            
            # 7. Instruções (posicionadas fora da moldura, na parte inferior da tela)
            instructions = [
                "↑/↓ ou mouse para navegar",
                "Enter/Espaço/Clique para selecionar",
                "ESC para voltar"
            ]
            if len(options) > items_per_page:
                instructions.insert(1, "PgUp/PgDown para páginas")
                instructions.insert(2, "Scroll do mouse para rolar")
            
            for i, instruction in enumerate(instructions):
                self.set_texto(instruction, 10, self.height - 120 + i * 20, self.WHITE)
            
            pygame.display.flip()
            clock.tick(60)

    def set_menu_combate(self, title: str, status_info: dict, opcoes_combate: list, selected: int = 0) -> int:
        """
        Menu específico para combate com informações de status responsivas
        
        Args:
            title: Título do combate
            status_info: Dicionário com informações do personagem e monstro
            opcoes_combate: Lista de opções de combate
            selected: Opção selecionada atualmente
            
        Returns:
            int: Índice da opção selecionada ou -1 para sair
        """
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        return -1
                    elif event.key == pygame.K_UP:
                        selected = (selected - 1) % len(opcoes_combate)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(opcoes_combate)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return selected
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Botão esquerdo
                        mouse_pos = event.pos
                        button_rects = self._get_combat_button_rects(opcoes_combate)
                        for i, (rect, _) in enumerate(button_rects):
                            if rect.collidepoint(mouse_pos):
                                return i
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = event.pos
                    button_rects = self._get_combat_button_rects(opcoes_combate)
                    for i, (rect, _) in enumerate(button_rects):
                        if rect.collidepoint(mouse_pos):
                            selected = i
            
            # Renderização
            self._render_combat_screen(title, status_info, opcoes_combate, selected)
            
            pygame.display.flip()
            clock.tick(60)
    
    def _render_combat_screen(self, title: str, status_info: dict, opcoes_combate: list, selected: int):
        """Renderiza a tela de combate com responsividade"""

        caminho_fundo = os.path.join(os.path.dirname(__file__), '../../../assets/fundo.png')
        imagem_fundo = self.carregar_imagem_fundo(caminho_fundo)
        
        if imagem_fundo:
            self.set_plano_fundo(imagem_fundo)
        else:
            self.screen.fill(self.BLACK)
        
        # Configurar moldura principal responsiva
        moldura_largura = min(self.width * 0.9, 1400)  # Máximo 1400px
        moldura_altura = min(self.height * 0.85, 900)   # Máximo 900px
        moldura_x = (self.width - moldura_largura) // 2
        moldura_y = (self.height - moldura_altura) // 2
        moldura_rect = pygame.Rect(moldura_x, moldura_y, moldura_largura, moldura_altura)
        
        # Desenhar sombra e moldura
        self.desenhar_sombra_moldura(moldura_rect)
        pygame.draw.rect(self.screen, self.BLACK, moldura_rect)
        pygame.draw.rect(self.screen, self.MARROM, moldura_rect, 3)
        
        # Título do combate
        titulo_y = moldura_y + moldura_altura * 0.06
        self.set_titulo_na_moldura(title, moldura_rect.centerx, titulo_y)
        
        # Renderizar seções de status
        self._render_monster_status(moldura_rect, status_info.get('monstro', {}))
        self._render_player_status(moldura_rect, status_info.get('personagem', {}))
        
        # Renderizar botões de ação
        self._render_combat_buttons(moldura_rect, opcoes_combate, selected)
    
    def _render_monster_status(self, moldura_rect: pygame.Rect, monstro_info: dict):
        """Renderiza seção de status do monstro"""
        section_y = moldura_rect.y + moldura_rect.height * 0.15
        section_height = moldura_rect.height * 0.25
        
        # Título da seção
        self.set_texto("=== STATUS DO MONSTRO ===", 
                      moldura_rect.x + 20, section_y, self.MARROM)
        
        # Informações básicas
        info_y = section_y + 35
        especie = monstro_info.get('especie', 'Desconhecido')
        vida_atual = monstro_info.get('vida_atual', 0)
        vida_maxima = monstro_info.get('vida_maxima', 1)
        
        # Usar fonte menor se o texto for muito grande
        especie_display = especie if len(especie) <= 20 else especie[:17] + "..."
        
        self.set_texto(f"Espécie: {especie_display}", 
                      moldura_rect.x + 20, info_y, self.WHITE)
        self.set_texto(f"Vida: {vida_atual}/{vida_maxima}", 
                      moldura_rect.x + 20, info_y + 30, self.WHITE)
        
        # Barra de vida responsiva
        barra_x = moldura_rect.x + min(300, moldura_rect.width * 0.35)
        barra_y = info_y + 30
        barra_width = moldura_rect.width - (barra_x - moldura_rect.x) - 20
        barra_height = max(15, int(moldura_rect.height * 0.02))
        
        # Garantir que a barra não saia da moldura
        barra_width = min(barra_width, moldura_rect.right - barra_x - 20)
        
        # Fundo da barra
        pygame.draw.rect(self.screen, self.DARK_GRAY, (barra_x, barra_y, barra_width, barra_height))
        
        # Barra de vida
        if vida_maxima > 0:
            vida_percent = vida_atual / vida_maxima
            vida_width = int(barra_width * vida_percent)
            cor_vida = self.RED if vida_percent < 0.3 else (255, 165, 0) if vida_percent < 0.6 else (0, 255, 0)
            pygame.draw.rect(self.screen, cor_vida, (barra_x, barra_y, vida_width, barra_height))
    
    def _render_player_status(self, moldura_rect: pygame.Rect, personagem_info: dict):
        """Renderiza seção de status do personagem"""
        section_y = moldura_rect.y + moldura_rect.height * 0.45
        
        # Título da seção
        self.set_texto("=== SEU PERSONAGEM ===", 
                      moldura_rect.x + 20, section_y, self.MARROM)
        
        # Informações do personagem
        info_y = section_y + 35
        nome = personagem_info.get('nome', 'Desconhecido')
        nivel = personagem_info.get('nivel', 1)
        exp_atual = personagem_info.get('exp_atual', 0)
        exp_maxima = personagem_info.get('exp_maxima', 100)
        vida_atual = personagem_info.get('vida_atual', 0)
        vida_maxima = personagem_info.get('vida_maxima', 1)
        stamina_atual = personagem_info.get('stamina_atual', 0)
        stamina_maxima = personagem_info.get('stamina_maxima', 1)
        
        # Usar fonte menor se necessário
        nome_display = nome if len(nome) <= 15 else nome[:12] + "..."
        
        self.set_texto(f"Nome: {nome_display} | Nível: {nivel}", 
                      moldura_rect.x + 20, info_y, self.WHITE)
        self.set_texto(f"EXP: {exp_atual}/{exp_maxima}", 
                      moldura_rect.x + 20, info_y + 25, self.WHITE)
        self.set_texto(f"Vida: {vida_atual}/{vida_maxima}", 
                      moldura_rect.x + 20, info_y + 50, self.WHITE)
        self.set_texto(f"Stamina: {stamina_atual}/{stamina_maxima}", 
                      moldura_rect.x + 20, info_y + 75, self.WHITE)
        
        # Barras responsivas
        barra_x = moldura_rect.x + min(350, moldura_rect.width * 0.4)
        barra_width = moldura_rect.width - (barra_x - moldura_rect.x) - 20
        barra_height = max(12, int(moldura_rect.height * 0.015))
        
        # Garantir que não saia da moldura
        barra_width = min(barra_width, moldura_rect.right - barra_x - 20)
        
        # Barra de vida
        pygame.draw.rect(self.screen, self.DARK_GRAY, (barra_x, info_y + 50, barra_width, barra_height))
        if vida_maxima > 0:
            vida_percent = vida_atual / vida_maxima
            vida_width = int(barra_width * vida_percent)
            cor_vida = self.RED if vida_percent < 0.3 else (255, 165, 0) if vida_percent < 0.6 else (0, 255, 0)
            pygame.draw.rect(self.screen, cor_vida, (barra_x, info_y + 50, vida_width, barra_height))
        
        # Barra de stamina
        pygame.draw.rect(self.screen, self.DARK_GRAY, (barra_x, info_y + 75, barra_width, barra_height))
        if stamina_maxima > 0:
            stamina_percent = stamina_atual / stamina_maxima
            stamina_width = int(barra_width * stamina_percent)
            pygame.draw.rect(self.screen, self.BLUE, (barra_x, info_y + 75, stamina_width, barra_height))
    
    def _render_combat_buttons(self, moldura_rect: pygame.Rect, opcoes: list, selected: int):
        """Renderiza botões de combate com seleção visual"""
        acoes_y_start = moldura_rect.y + moldura_rect.height * 0.72
        
        # Título das ações
        self.set_texto("=== ESCOLHA SUA AÇÃO ===", 
                      moldura_rect.x + 20, acoes_y_start, self.MARROM)
        
        # Calcular tamanhos responsivos
        available_width = moldura_rect.width - 40
        cols = 2 if len(opcoes) > 3 else 1
        button_width = (available_width - 20) // cols
        button_height = max(40, int(moldura_rect.height * 0.05))
        spacing = 10
        
        # Desenhar botões
        for i, opcao in enumerate(opcoes):
            col = i % cols
            row = i // cols
            
            x = moldura_rect.x + 20 + col * (button_width + 20)
            y = acoes_y_start + 40 + row * (button_height + spacing)
            
            # Cores baseadas na seleção
            is_selected = (i == selected)
            bg_color = self.MARROM if is_selected else self.DARK_GRAY
            border_color = self.WHITE if is_selected else self.GRAY
            text_color = self.WHITE
            
            button_rect = pygame.Rect(x, y, button_width, button_height)
            
            # Desenhar botão com destaque se selecionado
            pygame.draw.rect(self.screen, bg_color, button_rect)
            border_width = 3 if is_selected else 2
            pygame.draw.rect(self.screen, border_color, button_rect, border_width)
            
            # Texto do botão com fonte adaptativa
            font = self.font_button if len(opcao) <= 25 else self.font_text
            text_surface = self.renderizar_texto(opcao, font, text_color)
            text_rect = text_surface.get_rect(center=button_rect.center)
            
            # Garantir que o texto caiba no botão
            if text_surface.get_width() > button_width - 10:
                # Usar fonte menor
                text_surface = self.renderizar_texto(opcao, self.font_small, text_color)
                text_rect = text_surface.get_rect(center=button_rect.center)
            
            self.screen.blit(text_surface, text_rect)
    
    def _get_combat_button_rects(self, opcoes: list) -> list:
        """Retorna lista de retângulos dos botões para detecção de clique"""
        moldura_largura = min(self.width * 0.9, 1400)
        moldura_altura = min(self.height * 0.85, 900)
        moldura_x = (self.width - moldura_largura) // 2
        moldura_y = (self.height - moldura_altura) // 2
        moldura_rect = pygame.Rect(moldura_x, moldura_y, moldura_largura, moldura_altura)
        
        acoes_y_start = moldura_rect.y + moldura_rect.height * 0.72
        available_width = moldura_rect.width - 40
        
        # Determinar layout como no método de renderização
        if moldura_rect.width < 500 or len(opcoes) <= 2:
            cols = 1
        elif len(opcoes) <= 4:
            cols = 2
        else:
            cols = min(3, len(opcoes))
        
        button_width = (available_width - (cols - 1) * 15) // cols
        button_height = max(40, min(50, int(moldura_rect.height * 0.3 / ((len(opcoes) + cols - 1) // cols))))
        spacing_y = 8
        
        button_rects = []
        for i, opcao in enumerate(opcoes):
            col = i % cols
            row = i // cols
            
            x = moldura_rect.x + 15 + col * (button_width + 15)
            y = acoes_y_start + 35 + row * (button_height + spacing_y)
            
            if y + button_height <= moldura_rect.bottom - 10:  # Só adicionar se couber
                button_rect = pygame.Rect(x, y, button_width, button_height)
                button_rects.append((button_rect, opcao))
        
        return button_rects
    
    def combate_pygame_completo(self, id_personagem, personagem_info, monstro_info, monstro_stats, opcoes_combate, selected=0):
        """
        Menu de combate completo integrado e responsivo
        
        Args:
            id_personagem: ID do personagem
            personagem_info: Dicionário com informações do personagem
            monstro_info: Dicionário com informações do monstro
            monstro_stats: Dicionário com stats atuais do monstro
            opcoes_combate: Lista de opções de combate disponíveis
            selected: Opção atualmente selecionada
            
        Returns:
            int: Índice da opção selecionada, -1 para fugir/sair
        """
        clock = pygame.time.Clock()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return -1
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                        return -1  # Fugir
                    elif event.key == pygame.K_UP:
                        selected = (selected - 1) % len(opcoes_combate)
                    elif event.key == pygame.K_DOWN:
                        selected = (selected + 1) % len(opcoes_combate)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        return selected
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Botão esquerdo
                        mouse_pos = event.pos
                        button_rects = self._get_combat_button_rects_responsive(opcoes_combate)
                        for i, (rect, _) in enumerate(button_rects):
                            if rect.collidepoint(mouse_pos):
                                return i
                elif event.type == pygame.MOUSEMOTION:
                    mouse_pos = event.pos
                    button_rects = self._get_combat_button_rects_responsive(opcoes_combate)
                    for i, (rect, _) in enumerate(button_rects):
                        if rect.collidepoint(mouse_pos):
                            selected = i

            # Renderização completa da tela de combate
            self._render_combat_screen_responsive(personagem_info, monstro_info, monstro_stats, opcoes_combate, selected)
            
            pygame.display.flip()
            clock.tick(60)

    def _render_combat_screen_responsive(self, personagem_info, monstro_info, monstro_stats, opcoes_combate, selected):
        """Renderiza a tela de combate completa de forma responsiva"""
        # Carregar fundo
        caminho_fundo = os.path.join(os.path.dirname(__file__), '../../../assets/fundo.png')
        imagem_fundo = self.carregar_imagem_fundo(caminho_fundo)
        
        if imagem_fundo:
            self.set_plano_fundo(imagem_fundo)
        else:
            self.screen.fill(self.BLACK)
        
        # Configurar moldura principal responsiva (mais conservadora para evitar overflow)
        moldura_largura = min(self.width * 0.85, 1200)  # Reduzido de 0.9 para 0.85
        moldura_altura = min(self.height * 0.8, 800)    # Reduzido de 0.85 para 0.8
        moldura_x = (self.width - moldura_largura) // 2
        moldura_y = (self.height - moldura_altura) // 2
        moldura_rect = pygame.Rect(moldura_x, moldura_y, moldura_largura, moldura_altura)
        
        # Desenhar sombra e moldura
        self.desenhar_sombra_moldura(moldura_rect)
        pygame.draw.rect(self.screen, self.BLACK, moldura_rect)
        pygame.draw.rect(self.screen, self.MARROM, moldura_rect, 3)
        
        # Título do combate
        titulo_y = moldura_y + moldura_altura * 0.05
        self.set_titulo_na_moldura("⚔️ COMBATE ⚔️", moldura_rect.centerx, titulo_y)
        
        # Renderizar seções de status
        self._render_monster_status_responsive(moldura_rect, monstro_info, monstro_stats)
        self._render_player_status_responsive(moldura_rect, personagem_info)
        
        # Renderizar botões de ação
        self._render_combat_buttons_responsive(moldura_rect, opcoes_combate, selected)

    def _render_monster_status_responsive(self, moldura_rect: pygame.Rect, monstro_info: dict, monstro_stats: dict):
        """Renderiza seção de status do monstro de forma responsiva"""
        section_y = moldura_rect.y + moldura_rect.height * 0.12
        
        # Título da seção
        self.set_texto("=== STATUS DO MONSTRO ===", 
                      moldura_rect.x + 15, section_y, self.MARROM)
        
        # Informações básicas
        info_y = section_y + 30
        especie = monstro_info.get('especie', 'Desconhecido')
        vida_atual = monstro_stats.get('vida_atual', 0)
        vida_maxima = monstro_stats.get('vida_maxima', 1)
        
        # Truncar nome da espécie se muito longo para caber na moldura
        max_chars = max(15, int(moldura_rect.width / 30))  # Baseado na largura da moldura
        especie_display = especie if len(especie) <= max_chars else especie[:max_chars-3] + "..."
        
        self.set_texto(f"Espécie: {especie_display}", 
                      moldura_rect.x + 15, info_y, self.WHITE)
        self.set_texto(f"Vida: {vida_atual}/{vida_maxima}", 
                      moldura_rect.x + 15, info_y + 25, self.WHITE)
        
        # Barra de vida responsiva - garantir que não ultrapasse a moldura
        barra_start_x = moldura_rect.x + min(250, moldura_rect.width * 0.3)
        barra_y = info_y + 25
        barra_max_width = moldura_rect.right - barra_start_x - 20  # 20px de margem direita
        barra_width = max(100, min(barra_max_width, moldura_rect.width * 0.4))  # Entre 100px e 40% da moldura
        barra_height = max(12, int(moldura_rect.height * 0.015))
        
        # Fundo da barra
        pygame.draw.rect(self.screen, self.DARK_GRAY, (barra_start_x, barra_y, barra_width, barra_height))
        
        # Barra de vida
        if vida_maxima > 0:
            vida_percent = vida_atual / vida_maxima
            vida_width = int(barra_width * vida_percent)
            cor_vida = self.RED if vida_percent < 0.3 else (255, 165, 0) if vida_percent < 0.6 else (0, 255, 0)
            pygame.draw.rect(self.screen, cor_vida, (barra_start_x, barra_y, vida_width, barra_height))

    def _render_player_status_responsive(self, moldura_rect: pygame.Rect, personagem_info: dict):
        """Renderiza seção de status do personagem de forma responsiva"""
        section_y = moldura_rect.y + moldura_rect.height * 0.35
        
        # Título da seção
        self.set_texto("=== SEU PERSONAGEM ===", 
                      moldura_rect.x + 15, section_y, self.MARROM)
        
        # Informações do personagem
        info_y = section_y + 30
        nome = personagem_info.get('nome', 'Desconhecido')
        nivel = personagem_info.get('nivel', 1)
        exp_atual = personagem_info.get('exp_atual', 0)
        exp_maxima = personagem_info.get('exp_maxima', 100)
        vida_atual = personagem_info.get('vida_atual', 0)
        vida_maxima = personagem_info.get('vida_maxima', 1)
        stamina_atual = personagem_info.get('stamina_atual', 0)
        stamina_maxima = personagem_info.get('stamina_maxima', 1)
        
        # Truncar nome se muito longo
        max_chars = max(12, int(moldura_rect.width / 40))
        nome_display = nome if len(nome) <= max_chars else nome[:max_chars-3] + "..."
        
        # Usar layout condensado se moldura for pequena
        if moldura_rect.width < 600:
            self.set_texto(f"{nome_display} (Nv.{nivel})", 
                          moldura_rect.x + 15, info_y, self.WHITE)
            self.set_texto(f"EXP: {exp_atual}/{exp_maxima}", 
                          moldura_rect.x + 15, info_y + 20, self.WHITE)
            self.set_texto(f"Vida: {vida_atual}/{vida_maxima}", 
                          moldura_rect.x + 15, info_y + 40, self.WHITE)
            self.set_texto(f"Stamina: {stamina_atual}/{stamina_maxima}", 
                          moldura_rect.x + 15, info_y + 60, self.WHITE)
            line_spacing = 20
        else:
            self.set_texto(f"Nome: {nome_display} | Nível: {nivel}", 
                          moldura_rect.x + 15, info_y, self.WHITE)
            self.set_texto(f"EXP: {exp_atual}/{exp_maxima}", 
                          moldura_rect.x + 15, info_y + 25, self.WHITE)
            self.set_texto(f"Vida: {vida_atual}/{vida_maxima}", 
                          moldura_rect.x + 15, info_y + 50, self.WHITE)
            self.set_texto(f"Stamina: {stamina_atual}/{stamina_maxima}", 
                          moldura_rect.x + 15, info_y + 75, self.WHITE)
            line_spacing = 25
        
        # Barras responsivas
        barra_start_x = moldura_rect.x + min(280, moldura_rect.width * 0.35)
        barra_max_width = moldura_rect.right - barra_start_x - 20
        barra_width = max(80, min(barra_max_width, moldura_rect.width * 0.35))
        barra_height = max(10, int(moldura_rect.height * 0.012))
        
        # Barra de vida
        vida_y = info_y + (40 if moldura_rect.width < 600 else 50)
        pygame.draw.rect(self.screen, self.DARK_GRAY, (barra_start_x, vida_y, barra_width, barra_height))
        if vida_maxima > 0:
            vida_percent = vida_atual / vida_maxima
            vida_width = int(barra_width * vida_percent)
            cor_vida = self.RED if vida_percent < 0.3 else (255, 165, 0) if vida_percent < 0.6 else (0, 255, 0)
            pygame.draw.rect(self.screen, cor_vida, (barra_start_x, vida_y, vida_width, barra_height))
        
        # Barra de stamina
        stamina_y = info_y + (60 if moldura_rect.width < 600 else 75)
        pygame.draw.rect(self.screen, self.DARK_GRAY, (barra_start_x, stamina_y, barra_width, barra_height))
        if stamina_maxima > 0:
            stamina_percent = stamina_atual / stamina_maxima
            stamina_width = int(barra_width * stamina_percent)
            pygame.draw.rect(self.screen, self.BLUE, (barra_start_x, stamina_y, stamina_width, barra_height))

    def _render_combat_buttons_responsive(self, moldura_rect: pygame.Rect, opcoes: list, selected: int):
        """Renderiza botões de combate com seleção visual e layout responsivo"""
        acoes_y_start = moldura_rect.y + moldura_rect.height * 0.65
        
        # Título das ações
        self.set_texto("=== ESCOLHA SUA AÇÃO ===", 
                      moldura_rect.x + 15, acoes_y_start, self.MARROM)
        
        # Calcular layout responsivo
        available_width = moldura_rect.width - 30
        available_height = moldura_rect.height * 0.3
        
        # Determinar número de colunas baseado na largura e quantidade de opções
        if moldura_rect.width < 500 or len(opcoes) <= 2:
            cols = 1
        elif len(opcoes) <= 4:
            cols = 2
        else:
            cols = min(3, len(opcoes))
        
        button_width = (available_width - (cols - 1) * 15) // cols
        button_height = max(35, min(50, int(available_height / ((len(opcoes) + cols - 1) // cols))))
        spacing_y = 8
        
        # Desenhar botões
        for i, opcao in enumerate(opcoes):
            col = i % cols
            row = i // cols
            
            x = moldura_rect.x + 15 + col * (button_width + 15)
            y = acoes_y_start + 35 + row * (button_height + spacing_y)
            
            # Verificar se o botão cabe na moldura
            if y + button_height > moldura_rect.bottom - 10:
                break  # Não desenhar se não couber
            
            # Cores baseadas na seleção com maior contraste
            is_selected = (i == selected)
            if is_selected:
                bg_color = self.MARROM
                border_color = self.WHITE
                text_color = self.WHITE
                border_width = 4
            else:
                bg_color = self.DARK_GRAY
                border_color = self.GRAY
                text_color = self.WHITE
                border_width = 2
            
            button_rect = pygame.Rect(x, y, button_width, button_height)
            
            # Desenhar botão com destaque visual melhorado
            pygame.draw.rect(self.screen, bg_color, button_rect)
            pygame.draw.rect(self.screen, border_color, button_rect, border_width)
            
            # Adicionar brilho se selecionado
            if is_selected:
                # Criar efeito de brilho
                highlight_rect = pygame.Rect(x + 2, y + 2, button_width - 4, button_height - 4)
                pygame.draw.rect(self.screen, (255, 255, 255, 50), highlight_rect, 1)
            
            # Texto do botão com fonte adaptativa
            font = self.font_button
            text_surface = self.renderizar_texto(opcao, font, text_color)
            
            # Ajustar fonte se o texto não couber
            while text_surface.get_width() > button_width - 10 and font != self.font_small:
                if font == self.font_button:
                    font = self.font_text
                elif font == self.font_text:
                    font = self.font_small
                text_surface = self.renderizar_texto(opcao, font, text_color)
            
            # Se ainda não couber, truncar o texto
            if text_surface.get_width() > button_width - 10:
                truncated_text = opcao
                while font.size(truncated_text + "...")[0] > button_width - 10 and len(truncated_text) > 3:
                    truncated_text = truncated_text[:-1]
                text_surface = self.renderizar_texto(truncated_text + "...", font, text_color)
            
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)

    def _get_combat_button_rects_responsive(self, opcoes: list) -> list:
        """Retorna lista de retângulos dos botões para detecção de clique responsiva"""
        moldura_largura = min(self.width * 0.85, 1200)
        moldura_altura = min(self.height * 0.8, 800)
        moldura_x = (self.width - moldura_largura) // 2
        moldura_y = (self.height - moldura_altura) // 2
        moldura_rect = pygame.Rect(moldura_x, moldura_y, moldura_largura, moldura_altura)
        
        acoes_y_start = moldura_rect.y + moldura_rect.height * 0.65
        available_width = moldura_rect.width - 30
        
        # Determinar layout como no método de renderização
        if moldura_rect.width < 500 or len(opcoes) <= 2:
            cols = 1
        elif len(opcoes) <= 4:
            cols = 2
        else:
            cols = min(3, len(opcoes))
        
        button_width = (available_width - (cols - 1) * 15) // cols
        button_height = max(35, min(50, int(moldura_rect.height * 0.3 / ((len(opcoes) + cols - 1) // cols))))
        spacing_y = 8
        
        button_rects = []
        for i, opcao in enumerate(opcoes):
            col = i % cols
            row = i // cols
            
            x = moldura_rect.x + 15 + col * (button_width + 15)
            y = acoes_y_start + 35 + row * (button_height + spacing_y)
            
            if y + button_height <= moldura_rect.bottom - 10:  # Só adicionar se couber
                button_rect = pygame.Rect(x, y, button_width, button_height)
                button_rects.append((button_rect, opcao))
        
        return button_rects

