from simple_term_menu import TerminalMenu
from game.src.database import criar_cursor
from game.src.limpar_tela import limpar_tela
from game.src.ascii_art import salas
from game.src.operadores.Sala.print_mapa import print_mapa

def menu_acoes(id_personagem):
    print_mapa(id_personagem)
    opcoes = ["Mover", "Abrir Inventário","Visualizar Loja","Sair"] # quando for fazer a lógica de atacar monstros colocar aqui uma opção "Atacar Monstro"
    menu = TerminalMenu(
        opcoes,
        menu_cursor_style=("fg_green", "bold"),
        menu_highlight_style=("fg_green", "bold"),
        clear_screen=False
    )

    while True:
        cursor = criar_cursor()
        opcao = menu.show()
        limpar_tela()
        print(opcao)

        if opcao == 0:
            limpar_tela()
            return 'mover'
        elif opcao == 1:
            limpar_tela()
            return "abrir inventário"
            
        elif opcao == 2:
            limpar_tela()
            return "loja"
        
        elif opcao == 3:
            limpar_tela()
            return "sair"
