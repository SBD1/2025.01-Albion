from operadores.Menus.estrutura_menu_pygame import MenuPyGame
from operadores.Personagem.calcular_atributos import calcular_atributos_totais_personagem
from database import criar_cursor
import pygame
import os
import sys

def obter_info_personagem(id_personagem):
    """Obtém as informações completas do personagem com atributos calculados corretamente"""
    cursor = criar_cursor()
    
    try:
        # Primeiro obter informações da função SQL existente
        cursor.execute("SELECT * FROM f_get_info_personagem(%s);", (id_personagem,))
        resultado = cursor.fetchone()
        
        if resultado:
            # Agora calcular os atributos totais corretos (incluindo equipamentos)
            atributos_totais = calcular_atributos_totais_personagem(id_personagem)
            
            if atributos_totais:
                # Sobrescrever os atributos com os valores calculados
                resultado_dict = dict(resultado)
                resultado_dict['ataque_fisico'] = atributos_totais['ataque_fisico']
                resultado_dict['defesa_fisica'] = atributos_totais['defesa_fisica'] 
                resultado_dict['defesa_magica'] = atributos_totais['defesa_magica']
                resultado_dict['vida_maxima'] = atributos_totais['vida_maxima']
                return resultado_dict
        
        return resultado
        
    except Exception as e:
        print(f"Erro ao obter informações do personagem: {e}")
        return None
    finally:
        cursor.close()

def formatar_info_personagem(info_personagem):
    """Formata as informações do personagem para exibição"""
    if not info_personagem:
        return "Informações não disponíveis"
    
    classe = info_personagem['classe']
    
    # Informações básicas do personagem
    info_basica = f"""═══════════════════════════════════════
🎮 PERFIL DO PERSONAGEM
═══════════════════════════════════════

👤 Nome: {info_personagem['nome']}
🏅 Classe: {classe}
⭐ Nível: {info_personagem['nivel']}
🪙 Ouro: {info_personagem['qtd_ouro']}

📊 EXPERIÊNCIA:
   Atual: {info_personagem['exp_atual']} / {info_personagem['exp_maxima']}

❤️ VIDA:
   Atual: {info_personagem['vida_atual']} / {info_personagem['vida_maxima']}

⚡ STAMINA:
   Atual: {info_personagem['stamina_atual']} / {info_personagem['stamina_maxima']}

⚔️ ATRIBUTOS DE COMBATE:
   Ataque Físico: {info_personagem['ataque_fisico']}
   Defesa Física: {info_personagem['defesa_fisica']}
   Defesa Mágica: {info_personagem['defesa_magica']}"""
    
    if classe == 'Zoiudo':
        if info_personagem['nome_fantasma']:
            info_basica += f"""

═══════════════════════════════════════
👻 INFORMAÇÕES DO FANTASMA:
═══════════════════════════════════════

   Nome: {info_personagem['nome_fantasma']}
   Nível: {info_personagem['nivel_fantasma']}
   
   Experiência: {info_personagem['exp_atual_fantasma']} / {info_personagem['exp_maxima_fantasma']}
   
   Vida: {info_personagem['vida_atual_fantasma']} / {info_personagem['vida_maxima_fantasma']}
   
   Ataque Físico: {info_personagem['ataque_fisico_fantasma']}
   Ataque Mágico: {info_personagem['ataque_magico_fantasma']}
   Defesa Física: {info_personagem['defesa_fisica_fantasma']}
   Defesa Mágica: {info_personagem['defesa_magica_fantasma']}"""
        else:
            info_basica += f"""

👻 FANTASMA: Nenhum fantasma vinculado"""
    
    elif classe == 'Espiritualista':
        info_basica += f"""

═══════════════════════════════════════
✨ ATRIBUTOS MÁGICOS:
═══════════════════════════════════════

   Mana: {info_personagem['mana_atual']} / {info_personagem['mana_total']}
   Ataque Mágico: {info_personagem['ataque_magico_espiritualista']}"""
    
    elif classe == 'Draconico':
        info_basica += f"""

═══════════════════════════════════════
🐉 TRANSFORMAÇÃO DRAGÃO:
═══════════════════════════════════════

   Custo de Stamina: {info_personagem['custo_stamina']}
   
   Bônus por Transformação:
   • Aumento de Vida: +{info_personagem['aumento_vida_atual']}
   • Aumento de Ataque: +{info_personagem['aumento_ataque_fisico']}"""
    
    elif classe == 'Titan':
        info_basica += f"""

═══════════════════════════════════════
🛡️ ESPECIALIZAÇÃO TITAN:
═══════════════════════════════════════

   Classe focada em combate corpo a corpo
   Pode equipar até 3 armas simultaneamente
   
   ⚔️ O ataque físico exibido já inclui todas as armas equipadas"""
    
    return info_basica

def menu_perfil_personagem_pygame(id_personagem):
    """Menu para visualizar perfil completo do personagem implementado em PyGame"""
    menu = MenuPyGame(title="Albion Online - Perfil do Personagem")
    
    # Obter informações do personagem
    info_personagem = obter_info_personagem(id_personagem)
    
    if not info_personagem:
        menu.feedback("Erro", "Não foi possível carregar as informações do personagem.", 3000)
        return "voltar"
    
    # Formatar informações para exibição
    info_formatada = formatar_info_personagem(info_personagem)
    classe = info_personagem['classe']
    nome = info_personagem['nome']
    
    # Criar menu personalizado apenas com informações (sem botão)
    clock = pygame.time.Clock()
    
    while True:
        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "voltar"
        
        # Renderização
        menu.screen.fill(menu.BLACK)
        
        # Título
        menu.set_titulo(f"PERFIL - {nome} ({classe})")
        
        # Subtítulo com informações (suporta múltiplas linhas)
        subtitle_lines = info_formatada.split('\n')
        for i, line in enumerate(subtitle_lines):
            subtitle_surface = menu.renderizar_texto(line, menu.font_text, menu.WHITE)
            subtitle_rect = subtitle_surface.get_rect(center=(menu.width // 2, 120 + i * 25))
            menu.screen.blit(subtitle_surface, subtitle_rect)
        
        # Instruções no final
        instructions = [
            "ESC para voltar"
        ]
        for i, instruction in enumerate(instructions):
            menu.set_texto(instruction, 10, menu.height - 40 + i * 20, menu.GRAY)
        
        pygame.display.flip()
        clock.tick(60)
