from operadores.Menus.estrutura_menu_pygame import MenuPyGame
from database import criar_cursor
from ascii_art import salas_conexoes

def get_info_sala(id_personagem):
    """Obtém informações da sala atual do personagem"""
    cursor = criar_cursor()
    cursor.execute(f"SELECT * FROM f_get_sala({id_personagem});")
    retorno = cursor.fetchone()
    cursor.connection.close()
    
    nome_sala = retorno['nome'] if retorno else "Desconhecida"
    return nome_sala

def menu_acoes_pygame(id_personagem):
    """Menu de ações implementado em PyGame - mantém o mesmo fluxo do original"""
    menu = MenuPyGame(title="Albion Online - Ações")
    
    while True:
        nome_sala = get_info_sala(id_personagem)
        
        # Opções do menu 
        opcoes = ["Mover", "Abrir Inventário", "Itens Equipados", "Visualizar Loja", "Visualizar Perfil", "Sair"]
        
        # Mostrar o menu com informações da sala
        opcao = menu.set_menu(
            title="MENU DE AÇÕES",
            options=opcoes,
            subtitle=f"Localização: {nome_sala}\nEscolha uma ação:"
        )
        
        if opcao == 0: 
            return 'mover'
        elif opcao == 1: 
            return "inventario" 
        elif opcao == 2:  
            return "equipados"  
        elif opcao == 3: 
            return "loja"  
        elif opcao == 4: 
            return "perfil"  
        elif opcao == 5 or opcao == -1: 
            return "sair"
