from simple_term_menu import TerminalMenu

def selecionar_personagem(rows):
    opcoes = [f"{row['nome']} (Nível {row['nivel']}) (Ouro: {row['qtd_ouro']})" for row in rows]
    menu = TerminalMenu(
        opcoes,
        title="Selecione um personagem:",
        menu_cursor_style=("fg_green", "bold"),
        menu_highlight_style=("fg_green", "bold"),
        clear_screen=False
    )
    
    idx = menu.show()
    
    if idx == -1:
        print("Nenhum personagem selecionado.")
        return None
    
    return rows[idx]['id_personagem']