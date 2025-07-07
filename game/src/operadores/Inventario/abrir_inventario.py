from simple_term_menu import TerminalMenu
from game.src.database import criar_cursor
from game.src.limpar_tela import limpar_tela


def abrir_inventario(id_personagem):
    cursor = criar_cursor()
    cursor.execute(f"SELECT * FROM f_consulta_inventario({id_personagem});")
    itens = cursor.fetchall()
    # print(itens)

    if itens: 
        opcoes_menu = []
        for item in itens:
            nome = item['nome_item']
            qtd = item['quantidade']
            desc = item['descricao']
            opcoes_menu.append(f"{nome} - {desc}")

        opcoes_menu.append("Voltar")
        
        menu = TerminalMenu(
            opcoes_menu,
            title="🧰 Seu Inventário:",
            menu_cursor_style=("fg_green", "bold"),
            menu_highlight_style=("fg_green", "bold"),
            clear_screen=False
        )

        acao = menu.show()
        if opcoes_menu[acao] == "voltar":
            return -1
        else:
            return itens[acao]['id_instancia'],itens[acao]['nome_item']
    else:
        opcoes_menu = ["Voltar"]
        menu = TerminalMenu(
            opcoes_menu,
            title="📦 Seu Inventário está vazio.",
            menu_cursor_style=("fg_green", "bold"),
            menu_highlight_style=("fg_green", "bold"),
            clear_screen=False
        )
        acao = menu.show()
        if acao == -1  or opcoes_menu[acao] == "Voltar":
            return "voltar"
        

