import time
import pygame
import os
from game.src.ascii_art import grids
from game.src.database import criar_cursor
from game.src.operadores.Combate.menu_combate import iniciar_combate
from game.src.limpar_tela import limpar_tela
from game.src.operadores.Grids.grid_ruina import main_grid_pygame_ruinas
from game.src.operadores.Grids.grid_floresta import main_grid_pygame_floresta
from game.src.operadores.Grids.grid_deserto import main_grid_pygame_deserto
from game.src.operadores.Grids.grid_pantano import main_grid_pygame_pantano
from game.src.operadores.Grids.grid_caverna import main_grid_pygame_caverna
from game.src.operadores.Grids.grid_praça_central import main_grid_pygame_praca
from game.src.operadores.Grids.grid_campos_congelados import main_grid_pygame_neve
from game.src.operadores.Grids.grid_montanha import main_grid_pygame_montanha
from game.src.operadores.Personagem.sprite_personagem import carregar_sprites_personagem, desenhar_personagem_sprite

def atualizar_sala(id_personagem, nova_sala_id):
    cursor = criar_cursor()
    try:
        cursor.execute("""
        UPDATE public.personagem
        SET id_sala = %s
        WHERE id_personagem = %s;
        """, (nova_sala_id, id_personagem))
        cursor.connection.commit()
        return nova_sala_id
    except Exception as e:
        print(f"Erro ao atualizar sala do personagem no banco de dados: {e}")
        return None

def get_sala_info(id_personagem):
    cursor = criar_cursor()
    cursor.execute("""
        SELECT s.id_sala, s.nome, s.conexao_norte, s.conexao_sul, s.conexao_leste, s.conexao_oeste
        FROM public.personagem p
        JOIN public.sala s ON p.id_sala = s.id_sala
        WHERE p.id_personagem = %s;
    """, (id_personagem,))
    return cursor.fetchone()

def get_next_sala_name(sala_id):
    if sala_id is None:
        return None
    cursor = criar_cursor()
    cursor.execute("SELECT nome FROM public.sala WHERE id_sala = %s;", (sala_id,))
    next_info = cursor.fetchone()
    return next_info['nome'] if next_info else f"Sala {sala_id}"

def buscar_monstros_sala(nome_sala):
    grid_data = grids[nome_sala]
    if isinstance(grid_data, list) and isinstance(grid_data[0], str):
        return []
    else:
        _, monstros = grid_data
        return monstros

def main_grid_pygame(nome_sala, sala_info, pos_jogador, monstros_sala, sprites_personagem, direcao_atual):
    # Seleciona a função correta para cada grid
    if nome_sala == "Ruínas Antigas":
        return main_grid_pygame_ruinas, {'sprites_personagem': sprites_personagem, 'direcao_atual': direcao_atual}
    elif nome_sala == "Floresta do Leste":
        return main_grid_pygame_floresta, {'sprites_personagem': sprites_personagem, 'direcao_atual': direcao_atual}
    elif nome_sala == "Deserto Escaldante":
        return main_grid_pygame_deserto, {'sprites_personagem': sprites_personagem, 'direcao_atual': direcao_atual}
    elif nome_sala == "Pântano Sombrio":
        return main_grid_pygame_pantano, {'sprites_personagem': sprites_personagem, 'direcao_atual': direcao_atual}
    elif nome_sala == "Caverna Sombria":
        return main_grid_pygame_caverna, {'sprites_personagem': sprites_personagem, 'direcao_atual': direcao_atual}
    elif nome_sala == "Praça Central":
        return main_grid_pygame_praca, {'sprites_personagem': sprites_personagem, 'direcao_atual': direcao_atual}
    elif nome_sala == "Campos Congelados":
        return main_grid_pygame_neve, {'sprites_personagem': sprites_personagem, 'direcao_atual': direcao_atual}
    elif nome_sala == "Montanha Nevada":
        return main_grid_pygame_montanha, {'sprites_personagem': sprites_personagem, 'direcao_atual': direcao_atual}
    else:
        raise Exception(f"Sala não implementada: {nome_sala}")

def iniciar_grid_pygame(id_personagem):
    # Inicializa pygame antes de carregar sprites
    pygame.init()
    
    # Carrega os sprites do personagem uma vez
    sprites_personagem = carregar_sprites_personagem()
    direcao_atual = 'baixo'  # Direção inicial do personagem
    
    while True:
        sala = get_sala_info(id_personagem)
        if not sala:
            print("Erro ao obter informações da sala")
            return "voltar"
        nome_sala = sala['nome']
        grid_data = grids[nome_sala]
        if isinstance(grid_data, list) and isinstance(grid_data[0], str):
            grid = [list(l) for l in grid_data]
            monstros_sala = []
        else:
            grid, monstros_sala = grid_data
        # Posição inicial do jogador
        pos_jogador = [7, 25] if len(grid[0]) > 25 else [len(grid)//2, len(grid[0])//2]
        # Carregar sprites do personagem uma vez por sala
        sprites_personagem = carregar_sprites_personagem()
        while True:
            # Renderiza o grid e captura eventos
            func_grid, extra_args = main_grid_pygame(nome_sala, sala, pos_jogador, monstros_sala, sprites_personagem, direcao_atual)
            resultado_tuple = func_grid(sala['nome'], **extra_args)  # Chama a função do grid com argumentos extras
            
            # Verificar se retornou tupla com resultado, direção e posição
            if resultado_tuple is None or not isinstance(resultado_tuple, tuple):
                print(f"[ERRO] Função de grid '{func_grid.__name__}' não retornou tupla esperada. Valor retornado: {resultado_tuple}")
                resultado, direcao_movimento, pos_jogador_atualizada, nova_direcao = None, None, pos_jogador, direcao_atual
            elif len(resultado_tuple) == 4:
                resultado, direcao_movimento, pos_jogador_atualizada, nova_direcao = resultado_tuple
                pos_jogador[:] = pos_jogador_atualizada  # Atualiza posição do jogador
                direcao_atual = nova_direcao  # Atualiza direção do personagem
            elif len(resultado_tuple) == 3:
                resultado, direcao_movimento, pos_jogador_atualizada = resultado_tuple
                pos_jogador[:] = pos_jogador_atualizada  # Atualiza posição do jogador
                # Mantém a direção atual se não foi retornada nova direção
            elif len(resultado_tuple) == 2:
                resultado, direcao_movimento = resultado_tuple
                pos_jogador_atualizada = pos_jogador
            else:
                print(f"[ERRO] Função de grid '{func_grid.__name__}' retornou tupla com tamanho inesperado: {len(resultado_tuple)}")
                resultado, direcao_movimento, pos_jogador_atualizada, nova_direcao = None, None, pos_jogador, direcao_atual
            
            # Verifica se o usuário apertou 'q' para voltar ao menu de ações
            if resultado == "voltar":
                limpar_tela()
                return "voltar"
            
            # Checa se encontrou monstro
            if resultado == "encontrou_monstro":
                limpar_tela()
                cursor_enc = criar_cursor()
                cursor_enc.execute(
                    "SELECT especie FROM public.npc WHERE id_sala = %s;",
                    (sala['id_sala'],)
                )
                info_npc = cursor_enc.fetchone() or {'especie': 'Desconhecida'}
                print(f"Você encontrou um monstro selvagem! Espécie: {info_npc['especie']}")
                time.sleep(2)
                limpar_tela()
                combate_result = iniciar_combate(id_personagem, sala['id_sala'])
                if combate_result == "mudar_sala":
                    break
                # Remove o monstro da lista após o combate
                if tuple(pos_jogador_atualizada) in monstros_sala:
                    monstros_sala.remove(tuple(pos_jogador_atualizada))
                    # Também remove do grid se estiver lá
                    if 0 <= pos_jogador_atualizada[0] < len(grid) and 0 <= pos_jogador_atualizada[1] < len(grid[0]):
                        grid[pos_jogador_atualizada[0]][pos_jogador_atualizada[1]] = " "
                continue  # Volta para o grid após o combate
            
            # Mudança de sala
            if resultado == "mudar_sala" and direcao_movimento:
                conexao = None
                if direcao_movimento == "norte" and sala['conexao_norte']:
                    conexao = sala['conexao_norte']
                elif direcao_movimento == "sul" and sala['conexao_sul']:
                    conexao = sala['conexao_sul']
                elif direcao_movimento == "leste" and sala['conexao_leste']:
                    conexao = sala['conexao_leste']
                elif direcao_movimento == "oeste" and sala['conexao_oeste']:
                    conexao = sala['conexao_oeste']
                if conexao:
                    nome_destino = get_next_sala_name(conexao)
                    pygame.quit()
                    print(f"Locomovendo para {nome_destino}")
                    time.sleep(1.5)
                    limpar_tela()
                    atualizar_sala(id_personagem, conexao)
                    break  # Sai do loop interno e recarrega a nova sala
                else:
                    print("Não há passagem nessa direção!")
                    time.sleep(1.5)
            # Se não houve mudança de sala, continua no loop

#if __name__ == "__main__":
    #iniciar_grid_pygame(1)  # Substitua 1 pelo ID do personagem desejado