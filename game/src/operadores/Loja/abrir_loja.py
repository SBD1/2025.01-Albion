from simple_term_menu import TerminalMenu
from game.src.database import criar_cursor
from game.src.limpar_tela import limpar_tela

def abrir_loja(id_personagem):
    cursor = criar_cursor()
    cursor.execute(f"SELECT nivel FROM public.personagem WHERE id_personagem = {id_personagem};")
    nivel_personagem = cursor.fetchone()['nivel']

    cursor.execute(f"SELECT qtd_ouro FROM public.personagem WHERE id_personagem = {id_personagem};")
    qtd_ouro = cursor.fetchone()['qtd_ouro']

    cursor.execute(f"SELECT * FROM f_consulta_loja({nivel_personagem});")
    itens = cursor.fetchall()

    if itens: 
        opcoes_menu = []
        for item in itens:
            nome = item['nome_item']
            preco = item['preco']
            nivel_minimo = item['nivel_minimo']
            opcoes_menu.append(f"${preco} - {nome} (Nível Mínimo: {nivel_minimo})")

        opcoes_menu.append("Voltar")

        menu = TerminalMenu(
            opcoes_menu,
            title=f"""💵 Loja:
Ouro atual: ${qtd_ouro}
Escolha um item para comprar:""",
            menu_cursor_style=("fg_green", "bold"),
            menu_highlight_style=("fg_green", "bold"),
            clear_screen=False
        )

        acao = menu.show()

        if acao == -1 or opcoes_menu[acao] == "Voltar":
            return "voltar"
        else:
            return itens[acao]['id_item'], itens[acao]['id_item']

    else:
        limpar_tela()
        opcoes_menu = ["Voltar"]
        menu = TerminalMenu(
            opcoes_menu,
            title="Você não possui nível suficiente para comprar itens. (Nível mínimo: 5)",
            menu_cursor_style=("fg_green", "bold"),
            menu_highlight_style=("fg_green", "bold"),
            clear_screen=False
        )
        acao = menu.show()
        if acao == -1  or opcoes_menu[acao] == "Voltar":
            return "voltar"
        