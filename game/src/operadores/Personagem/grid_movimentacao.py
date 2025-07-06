import curses
import os
import time
from game.src.ascii_art import grids
from game.src.database import criar_cursor
from game.src.operadores.Combate.menu_combate import iniciar_combate
from game.src.limpar_tela import limpar_tela

def renderizar_grid(stdscr, grid, posicao_jogador):
    stdscr.clear()
    curses.curs_set(0) 

    altura_terminal, largura_terminal = stdscr.getmaxyx()

    altura_grid = len(grid)
    largura_grid = len(grid[0]) * 2  

    offset_y = (altura_terminal - altura_grid) // 2
    offset_x = (largura_terminal - largura_grid) // 2

    x, y = posicao_jogador
    for i, linha in enumerate(grid):
        for j, celula in enumerate(linha):
            if (i, j) == (x, y):
                stdscr.addstr(offset_y + i, offset_x + j * 2, "@", curses.color_pair(1))  
            else:
                stdscr.addstr(offset_y + i, offset_x + j * 2, str(celula))  
    stdscr.refresh()  

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

def iniciar_grid(id_personagem):
    cursor = criar_cursor()
    cursor.execute(f"""
        SELECT s.id_sala, s.nome, s.conexao_norte, s.conexao_sul, s.conexao_leste, s.conexao_oeste
        FROM public.personagem p
        JOIN public.sala s ON p.id_sala = s.id_sala
        WHERE p.id_personagem = {id_personagem};
    """)
    sala = cursor.fetchone()
    grid_data = grids[sala['nome']]  
    
    if isinstance(grid_data, list) and isinstance(grid_data[0], str):
        grid = grid_data
        monstros_sala = [] 
    else:
        grid, monstros_sala = grid_data 
    
    posicao_jogador = [7,25]  

    def main(stdscr):
        result = None
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        stdscr.keypad(True) 
        stdscr.timeout(100) 

        while True:
            renderizar_grid(stdscr, grid, posicao_jogador)
            if tuple(posicao_jogador) in monstros_sala:
                curses.endwin()
                limpar_tela()
                # Tela de encontro de monstro
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
                    result = "mudar_sala"
                    break
                # Retorna ao modo curses após combate
                stdscr = curses.initscr()
                curses.curs_set(0)
                curses.start_color()
                curses.use_default_colors()
                curses.init_pair(1, curses.COLOR_GREEN, -1)
                stdscr.keypad(True)
                stdscr.timeout(100)
                monstros_sala.remove(tuple(posicao_jogador))
            key = stdscr.getch()

            if key == curses.KEY_UP:
                if posicao_jogador[0] > 1 and grid[posicao_jogador[0] - 1][posicao_jogador[1]] == ' ':
                    posicao_jogador[0] -= 1
                elif posicao_jogador[0] == 1 and posicao_jogador[1] == len(grid[0]) // 2:
                    if sala['conexao_norte'] is not None:
                        limpar_tela()
                        # Busca nome da sala destino
                        cursor_name = criar_cursor()
                        cursor_name.execute(
                            "SELECT nome FROM public.sala WHERE id_sala = %s;",
                            (sala['conexao_norte'],)
                        )
                        next_info = cursor_name.fetchone()
                        nome_destino = next_info['nome'] if next_info else f"Sala {sala['conexao_norte']}"
                        print(f"Locomovendo para {nome_destino}")
                        time.sleep(1.5)
                        atualizar_sala(id_personagem, sala['conexao_norte'])
                        result = "mudar_sala"
                        break

            elif key == curses.KEY_DOWN:
                if posicao_jogador[0] < len(grid) - 2 and grid[posicao_jogador[0] + 1][posicao_jogador[1]] == ' ':
                    posicao_jogador[0] += 1
                elif posicao_jogador[0] == len(grid) - 2 and posicao_jogador[1] == len(grid[0]) // 2:
                    if sala['conexao_sul'] is not None:
                        limpar_tela()
                        # Busca nome da sala destino
                        cursor_name = criar_cursor()
                        cursor_name.execute(
                            "SELECT nome FROM public.sala WHERE id_sala = %s;",
                            (sala['conexao_sul'],)
                        )
                        next_info = cursor_name.fetchone()
                        nome_destino = next_info['nome'] if next_info else f"Sala {sala['conexao_sul']}"
                        print(f"Locomovendo para {nome_destino}")
                        time.sleep(1.5)
                        atualizar_sala(id_personagem, sala['conexao_sul'])
                        result = "mudar_sala"
                        break 

            elif key == curses.KEY_LEFT:
                if posicao_jogador[1] > 1 and grid[posicao_jogador[0]][posicao_jogador[1] - 1] == ' ':
                    posicao_jogador[1] -= 1
                elif posicao_jogador[1] == 1 and posicao_jogador[0] == len(grid) // 2:
                    if sala['conexao_oeste'] is not None:
                        limpar_tela()
                        # Busca nome da sala destino
                        cursor_name = criar_cursor()
                        cursor_name.execute(
                            "SELECT nome FROM public.sala WHERE id_sala = %s;",
                            (sala['conexao_oeste'],)
                        )
                        next_info = cursor_name.fetchone()
                        nome_destino = next_info['nome'] if next_info else f"Sala {sala['conexao_oeste']}"
                        print(f"Locomovendo para {nome_destino}")
                        time.sleep(1.5)
                        atualizar_sala(id_personagem, sala['conexao_oeste'])
                        result = "mudar_sala"
                        break 

            elif key == curses.KEY_RIGHT:
                if posicao_jogador[1] < len(grid[0]) - 2 and grid[posicao_jogador[0]][posicao_jogador[1] + 1] == ' ':
                    posicao_jogador[1] += 1
                elif posicao_jogador[1] == len(grid[0]) - 2 and posicao_jogador[0] == len(grid) // 2:
                    if sala['conexao_leste'] is not None:
                        limpar_tela()
                        # Busca nome da sala destino
                        cursor_name = criar_cursor()
                        cursor_name.execute(
                            "SELECT nome FROM public.sala WHERE id_sala = %s;",
                            (sala['conexao_leste'],)
                        )
                        next_info = cursor_name.fetchone()
                        nome_destino = next_info['nome'] if next_info else f"Sala {sala['conexao_leste']}"
                        print(f"Locomovendo para {nome_destino}")
                        time.sleep(1.5)
                        atualizar_sala(id_personagem, sala['conexao_leste'])
                        result = "mudar_sala"
                        break 

            elif key == ord('q'):
                result = "voltar"
                break

        return result 

    try:
        resultado = curses.wrapper(main)
    except curses.error:
        resultado = "mudar_sala"
    return resultado
