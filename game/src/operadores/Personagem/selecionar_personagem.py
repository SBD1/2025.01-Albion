from simple_term_menu import TerminalMenu
def selecionar_personagem(rows,id_usuario, username):
    opcoes = [f"{row['nome']} ({row['especie']}) (Nível {row['nivel']}) (Ouro: {row['qtd_ouro']}) (Localizado em: {row['nome_sala']})" for row in rows]
    opcoes.append("Voltar")
    if rows is None or len(rows) == 0:
        menu = TerminalMenu(
            opcoes,
            title="❌ Nenhum personagem encontrado.\n",
            menu_cursor_style=("fg_green", "bold"),
            menu_highlight_style=("fg_green", "bold"),
            clear_screen=False)
    else:
        menu = TerminalMenu(
            opcoes,
            title="Selecione um personagem.\n",
            menu_cursor_style=("fg_green", "bold"),
            menu_highlight_style=("fg_green", "bold"),
            clear_screen=False)
    
    idx = menu.show()
    
    if opcoes[idx] == "Voltar":
        return None
    
    elif idx == -1:
        print(" ❌ Nenhum personagem selecionado.\n")
        return None
    
    return rows[idx]['id_personagem']