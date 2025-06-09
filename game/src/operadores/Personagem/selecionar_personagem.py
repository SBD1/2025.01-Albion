from simple_term_menu import TerminalMenu
from game.src.operadores.Personagem.menu_personagens import menu_personagens
def selecionar_personagem(rows,id_usuario,username):
    opcoes = [f"{row['nome']} (Nível {row['nivel']}) (Ouro: {row['qtd_ouro']})" for row in rows]
    opcoes.append("Voltar")
    if rows is None or len(rows) == 0:
        menu = TerminalMenu(
            opcoes,
            title="Nenhum personagem encontrado.\n",
            menu_cursor_style=("fg_green", "bold"),
            menu_highlight_style=("fg_green", "bold"),
            clear_screen=False)
    else:
        menu = TerminalMenu(
            opcoes,
            title="Selecione um personagem.",
            menu_cursor_style=("fg_green", "bold"),
            menu_highlight_style=("fg_green", "bold"),
            clear_screen=False)
    
    idx = menu.show()
    
    if opcoes[idx] == "Voltar":
        menu_personagens(id_usuario,username)
        return None
    elif idx == -1:
        print("Nenhum personagem selecionado.\n")
        return None
    
    return rows[idx]['id_personagem']