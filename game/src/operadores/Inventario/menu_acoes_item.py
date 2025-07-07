from simple_term_menu import TerminalMenu
from game.src.database import criar_cursor
from game.src.limpar_tela import limpar_tela
from game.src.operadores.Item.equipar_item import equipar_item
from game.src.operadores.Item.desequipar_item import desequipar_item
from game.src.operadores.Item.vender_item import vender_item


def menu_acoes_item(id_instancia_item):
    cursor = criar_cursor()

    cursor.execute(f"SELECT * FROM f_get_tipo_item({id_instancia_item});")
    tipo_item = cursor.fetchone()

    opcoes_menu = ["Equipar", "Desequipar", "Vender", "Voltar"]

    menu = TerminalMenu(
        opcoes_menu,
        title=f"⚙️ Ações para o item:",
        menu_cursor_style=("fg_green", "bold"),
        menu_highlight_style=("fg_green", "bold"),
        clear_screen=False
    )

    acao = menu.show()

    if acao == -1 or opcoes_menu[acao] == "Voltar":
        return "voltar"

    if opcoes_menu[acao] == "Equipar":
        equipar_item(cursor, id_instancia_item)
    elif opcoes_menu[acao] == "Desequipar":
        desequipar_item(cursor, id_instancia_item)
    elif opcoes_menu[acao] == "Vender":
        vender_item(cursor, id_instancia_item)

    return "voltar"