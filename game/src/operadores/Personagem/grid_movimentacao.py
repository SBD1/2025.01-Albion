import curses
import os
from game.src.ascii_art import grids
from game.src.database import criar_cursor

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

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

    def verificar_posicao_com_monstro(posicao_personagem, monstros):
        if posicao_personagem in monstros:
            print("Iniciando combate!")
            #iniciar_combate()  # Chama a interface de combate (a ser implementada)
            return True
        return False

    def main(stdscr):
        result = None
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_GREEN, -1)
        stdscr.keypad(True) 
        stdscr.timeout(100) 

        while True:
            renderizar_grid(stdscr, grid, posicao_jogador)
            key = stdscr.getch()

            #if verificar_posicao_com_monstro(tuple(posicao_jogador), monstros_sala):
            #   break 

            if key == curses.KEY_UP:
                if posicao_jogador[0] > 1 and grid[posicao_jogador[0] - 1][posicao_jogador[1]] == ' ':
                    posicao_jogador[0] -= 1
                elif posicao_jogador[0] == 1 and posicao_jogador[1] == len(grid[0]) // 2:
                    if sala['conexao_norte'] is not None:
                        atualizar_sala(id_personagem, sala['conexao_norte'])
                        result = "mudar_sala"
                        break

            elif key == curses.KEY_DOWN:
                if posicao_jogador[0] < len(grid) - 2 and grid[posicao_jogador[0] + 1][posicao_jogador[1]] == ' ':
                    posicao_jogador[0] += 1
                elif posicao_jogador[0] == len(grid) - 2 and posicao_jogador[1] == len(grid[0]) // 2:
                    if sala['conexao_sul'] is not None:
                        atualizar_sala(id_personagem, sala['conexao_sul'])
                        result = "mudar_sala"
                        break 

            elif key == curses.KEY_LEFT:
                if posicao_jogador[1] > 1 and grid[posicao_jogador[0]][posicao_jogador[1] - 1] == ' ':
                    posicao_jogador[1] -= 1
                elif posicao_jogador[1] == 1 and posicao_jogador[0] == len(grid) // 2:
                    if sala['conexao_oeste'] is not None:
                        atualizar_sala(id_personagem, sala['conexao_oeste'])
                        result = "mudar_sala"
                        break 

            elif key == curses.KEY_RIGHT:
                if posicao_jogador[1] < len(grid[0]) - 2 and grid[posicao_jogador[0]][posicao_jogador[1] + 1] == ' ':
                    posicao_jogador[1] += 1
                elif posicao_jogador[1] == len(grid[0]) - 2 and posicao_jogador[0] == len(grid) // 2:
                    if sala['conexao_leste'] is not None:
                        atualizar_sala(id_personagem, sala['conexao_leste'])
                        result = "mudar_sala"
                        break 

            elif key == ord('q'):
                result = "voltar"
                break

        return result 

    resultado = curses.wrapper(main)
    return resultado
