from operadores.Usuario.menu_usuario_pygame import menu_usuario_pygame
from operadores.Personagem.menu_personagem_pygame import menu_personagens_pygame
from operadores.Personagem.menu_movimentacao_personagem_pygame import iniciar_grid_pygame
from operadores.Personagem.menu_acoes_personagem_pygame import menu_acoes_pygame
from operadores.Inventario.menu_inventario_pygame import menu_inventario_pygame
from operadores.Inventario.menu_equipados_pygame import menu_equipados_pygame
from operadores.Loja.menu_loja_pygame import menu_loja_pygame
from operadores.Personagem.menu_perfil_personagem_pygame import menu_perfil_personagem_pygame

def main():
    while True:
        id_usuario, username = menu_usuario_pygame()
        
        if id_usuario is None:
            continue
        
        while True:
            # Menu de personagens agora retorna diretamente o personagem selecionado
            resultado = menu_personagens_pygame(id_usuario, username)
            
            if resultado == "voltar":
                break
            
            if resultado is not None:
                id_personagem = resultado['id_personagem'] 
                
                while True:
                    acao = menu_acoes_pygame(id_personagem)

                    if acao == "mover":
                        while True:
                            result_movimento = iniciar_grid_pygame(id_personagem)

                            if result_movimento == "voltar":
                                break
                
                    elif acao == "inventario":
                        # Usar o novo menu de inventário PyGame
                        menu_inventario_pygame(id_personagem)

                    elif acao == "equipados":
                        # Usar o novo menu de itens equipados PyGame
                        menu_equipados_pygame(id_personagem)

                    elif acao == "loja":
                        # Usar o novo menu de loja PyGame
                        menu_loja_pygame(id_personagem)

                    elif acao == "perfil":
                        # Usar o novo menu de perfil PyGame
                        menu_perfil_personagem_pygame(id_personagem)
                        
                    elif acao == "sair":
                        break
    
if __name__ == "__main__":
    main()