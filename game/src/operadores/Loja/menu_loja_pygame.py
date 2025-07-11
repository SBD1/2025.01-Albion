from operadores.Menus.estrutura_menu_pygame import MenuPyGame
from operadores.Loja.comprar_item import comprar_item
from database import criar_cursor

def obter_itens_loja(id_personagem):
    """Obtém os itens da loja - versão adaptada da função original"""
    cursor = criar_cursor()
    
    # Obter nível e ouro do personagem
    cursor.execute(f"SELECT nivel, qtd_ouro FROM public.personagem WHERE id_personagem = {id_personagem};")
    dados_personagem = cursor.fetchone()
    nivel_personagem = dados_personagem['nivel']
    qtd_ouro = dados_personagem['qtd_ouro']
    
    # Obter itens da loja
    cursor.execute(f"SELECT * FROM f_consulta_loja({nivel_personagem});")
    itens = cursor.fetchall()
    
    cursor.close()
    return itens, qtd_ouro

def menu_loja_pygame(id_personagem):
    """Menu de loja implementado em PyGame - chama as funções existentes"""
    menu = MenuPyGame(title="Albion Online - Loja")
    
    while True:
        # Obter itens da loja e ouro do personagem
        itens, qtd_ouro = obter_itens_loja(id_personagem)
        
        # Verificar se há itens disponíveis
        if not itens or len(itens) == 0:
            menu.feedback(
                "Loja Indisponível",
                "Você não possui nível suficiente para comprar itens.\n(Nível mínimo: 5)",
                3000
            )
            return "voltar"
        
        # Preparar opções do menu
        opcoes_menu = []
        for item in itens:
            nome = item['nome_item']
            preco = item['preco']
            nivel_minimo = item['nivel_minimo']
            opcoes_menu.append(f"${preco} - {nome} (Nível Mín: {nivel_minimo})")
        
        opcoes_menu.append("Voltar")
        
        # Mostrar menu de seleção de item
        item_selecionado = menu.set_menu(
            title="LOJA",
            options=opcoes_menu,
            subtitle=f"Ouro atual: ${qtd_ouro}\nEscolha um item para comprar:"
        )
        
        # Verificar se usuário cancelou ou escolheu voltar
        if item_selecionado == -1 or item_selecionado == len(opcoes_menu) - 1:
            return "voltar"
        
        # Obter dados do item selecionado
        item_dados = itens[item_selecionado]
        id_item = item_dados['id_item']
        nome_item = item_dados['nome_item']
        preco = item_dados['preco']
        
        # Verificar se personagem tem ouro suficiente
        if qtd_ouro < preco:
            menu.feedback(
                "Ouro Insuficiente", 
                f"Você precisa de ${preco} para comprar '{nome_item}'.\nVocê tem apenas ${qtd_ouro}.",
                3000
            )
            continue
        
        # Confirmar compra
        confirmacao = menu.set_menu(
            title="CONFIRMAR COMPRA",
            options=["Sim, comprar item", "Cancelar"],
            subtitle=f"Item: {nome_item}\nPreço: ${preco}\nSeu ouro: ${qtd_ouro}\n\nConfirma a compra?"
        )
        
        if confirmacao == 0:  # Confirmar compra
            try:
                comprar_item(id_personagem, id_item)
                menu.feedback(
                    "Sucesso!", 
                    f"Você comprou '{nome_item}' por ${preco}!",
                    3000
                )
                # Continua no loop para permitir mais compras
            except Exception as e:
                menu.feedback("Erro", f"Erro ao comprar item:\n{str(e)}", 3000)
        # Se cancelar (confirmacao != 0), continua no loop para mostrar a loja novamente
