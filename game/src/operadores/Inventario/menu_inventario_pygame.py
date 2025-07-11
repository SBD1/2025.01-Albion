from operadores.Menus.estrutura_menu_pygame import MenuPyGame
from database import criar_cursor

def obter_itens_inventario(id_personagem):
    """Obtém os itens do inventário - versão adaptada da função original"""
    cursor = criar_cursor()
    cursor.execute(f"SELECT * FROM f_consulta_inventario({id_personagem});")
    itens = cursor.fetchall()
    cursor.close()
    return itens

def menu_inventario_pygame(id_personagem):
    """Menu de inventário implementado em PyGame - chama as funções existentes"""
    menu = MenuPyGame(title="Albion Online - Inventário")
    
    while True:
        # Obter itens do inventário usando a função adaptada
        itens = obter_itens_inventario(id_personagem)
        
        # Verificar se inventário está vazio
        if not itens or len(itens) == 0:
            menu.feedback("Aviso", "Seu inventário está vazio.", 2000)
            return "voltar"
        
        # Preparar opções do menu
        opcoes_menu = []
        for item in itens:
            nome = item['nome_item']
            qtd = item['quantidade']
            opcoes_menu.append(f"{nome}")
        
        opcoes_menu.append("Voltar")
        
        # Mostrar menu de seleção de item
        item_selecionado = menu.set_menu(
            title="SEU INVENTÁRIO",
            options=opcoes_menu,
            subtitle="Escolha um item para interagir:"
        )
        
        # Verificar se usuário cancelou ou escolheu voltar
        if item_selecionado == -1 or item_selecionado == len(opcoes_menu) - 1:
            return "voltar"
        
        # Obter dados do item selecionado
        item_dados = itens[item_selecionado]
        id_instancia_item = item_dados['id_instancia']
        nome_item = item_dados['nome_item']
        
        # Verificar se é consumível para determinar opções
        from operadores.Inventario.consumir_item import verificar_se_consumivel
        eh_consumivel = verificar_se_consumivel(id_instancia_item)
        
        # Mostrar opções de ação para o item selecionado
        if eh_consumivel:
            opcoes_acoes = ["Visualizar Atributos", "Usar", "Voltar ao Inventário"]
        else:
            opcoes_acoes = ["Visualizar Atributos", "Equipar", "Voltar ao Inventário"]
        
        acao_selecionada = menu.set_menu(
            title="AÇÕES DO ITEM",
            options=opcoes_acoes,
            subtitle=f"Item selecionado: {nome_item}\nEscolha uma ação:"
        )
        
        if acao_selecionada == -1 or acao_selecionada == 3:  # ESC ou Voltar ao Inventário
            continue  # Volta para mostrar o inventário novamente
        
        # Mapear ação selecionada para as funções existentes
        if acao_selecionada == 0:  # Visualizar Atributos
            from operadores.Inventario.visualizar_item import visualizar_atributos_item, formatar_atributos_item
            
            item_info, tipo_item = visualizar_atributos_item(id_instancia_item)
            
            if item_info:
                atributos_formatados = formatar_atributos_item(item_info, tipo_item)
                # Usar menu sem moldura (como inventário e loja)
                opcoes_visualizar = ["🔙 Voltar"]
                menu.set_menu(
                    title="ATRIBUTOS DO ITEM",
                    options=opcoes_visualizar,
                    subtitle=atributos_formatados
                )
            else:
                menu.feedback("Erro", f"Não foi possível carregar os atributos do item.\n{tipo_item}", 3000)
                
        elif acao_selecionada == 1:  # Equipar ou Usar
            if eh_consumivel:
                # Usar item consumível
                from operadores.Inventario.consumir_item import consumir_item
                sucesso, mensagem = consumir_item(id_personagem, id_instancia_item)
                
                if sucesso:
                    menu.feedback("Sucesso", mensagem, 3000)
                    # Continuar no loop para atualizar a lista de itens
                else:
                    menu.feedback("Erro", mensagem, 3000)
            else:
                # Equipar item - verificar se é Titan tentando equipar arma
                from operadores.Inventario.equipar_item import verificar_se_titan, verificar_tipo_item, equipar_item_slot_especifico, equipar_item
                
                eh_titan = verificar_se_titan(id_personagem)
                tipo_item = verificar_tipo_item(id_instancia_item)
                
                if eh_titan and tipo_item == 'Arma':
                    # Mostrar submenu para escolher slot de arma para Titans
                    opcoes_slots = [
                        "Equipar Slot 1 (Principal)",
                        "Equipar Slot Extra 2", 
                        "Equipar Slot Extra 3",
                        "Voltar"
                    ]
                    
                    slot_escolhido = menu.set_menu(
                        title="SLOTS DE ARMA - TITAN",
                        options=opcoes_slots,
                        subtitle=f"Escolha onde equipar: {nome_item}\nTitans podem equipar até 3 armas!"
                    )
                    
                    if slot_escolhido == -1 or slot_escolhido == 3:  # Cancelou ou voltou
                        continue
                    
                    # Mapear escolha para slot
                    slots_map = {
                        0: 'slot_arma',
                        1: 'slot_extra_arma_1', 
                        2: 'slot_extra_arma_2'
                    }
                    
                    slot_tipo = slots_map[slot_escolhido]
                    
                    cursor = criar_cursor()
                    try:
                        equipar_item_slot_especifico(cursor, id_personagem, id_instancia_item, slot_tipo)
                        slot_nome = opcoes_slots[slot_escolhido].replace("Equipar ", "")
                        menu.feedback("Sucesso", f"'{nome_item}' equipado no {slot_nome}!", 2000)
                    except Exception as e:
                        menu.feedback("Erro", f"Erro ao equipar item:\n{str(e)}", 3000)
                    finally:
                        cursor.close()
                else:
                    # Equipar normalmente (não-Titan ou não-arma)
                    cursor = criar_cursor()
                    try:
                        equipar_item(cursor, id_instancia_item)
                        menu.feedback("Sucesso", f"Item '{nome_item}' equipado!", 2000)
                    except Exception as e:
                        menu.feedback("Erro", f"Erro ao equipar item:\n{str(e)}", 3000)
                    finally:
                        cursor.close()
                
