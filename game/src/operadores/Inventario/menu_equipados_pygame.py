from operadores.Menus.estrutura_menu_pygame import MenuPyGame
from database import criar_cursor
from operadores.Inventario.visualizar_item import visualizar_atributos_item, formatar_atributos_item

def obter_classe_personagem(id_personagem):
    """Obtém a classe do personagem"""
    cursor = criar_cursor()
    
    try:
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN z.id_personagem IS NOT NULL THEN 'Zoiudo'
                    WHEN e.id_personagem IS NOT NULL THEN 'Espiritualista'
                    WHEN d.id_personagem IS NOT NULL THEN 'Draconico'
                    WHEN t.id_personagem IS NOT NULL THEN 'Titan'
                    ELSE 'Desconhecido'
                END AS classe
            FROM public.personagem p
                LEFT JOIN public.zoiudo z ON p.id_personagem = z.id_personagem
                LEFT JOIN public.espiritualista e ON p.id_personagem = e.id_personagem
                LEFT JOIN public.draconico d ON p.id_personagem = d.id_personagem
                LEFT JOIN public.titan t ON p.id_personagem = t.id_personagem
            WHERE p.id_personagem = %s;
        """, (id_personagem,))
        
        resultado = cursor.fetchone()
        return resultado['classe'] if resultado else 'Desconhecido'
        
    except Exception as e:
        return 'Desconhecido'
    finally:
        cursor.close()

def obter_itens_equipados(id_personagem):
    """Obtém os itens equipados pelo personagem"""
    cursor = criar_cursor()
    
    try:
        classe = obter_classe_personagem(id_personagem)
        
        query_base = """
            SELECT 
                ie.slot_arma,
                ie.slot_armadura_capacete,
                ie.slot_armadura_peitoral,
                ie.slot_armadura_escudo,
                i1.nome as nome_arma,
                i2.nome as nome_armadura_capacete,
                i3.nome as nome_armadura_peitoral,
                i4.nome as nome_armadura_escudo
        """
        
        joins_base = """
            FROM INVENTARIO_EQUIPADOS ie
            LEFT JOIN INSTANCIA_ITEM ii1 ON ie.slot_arma = ii1.id_instancia
            LEFT JOIN ITEM i1 ON ii1.id_item = i1.id_item
            LEFT JOIN INSTANCIA_ITEM ii2 ON ie.slot_armadura_capacete = ii2.id_instancia
            LEFT JOIN ITEM i2 ON ii2.id_item = i2.id_item
            LEFT JOIN INSTANCIA_ITEM ii3 ON ie.slot_armadura_peitoral = ii3.id_instancia
            LEFT JOIN ITEM i3 ON ii3.id_item = i3.id_item
            LEFT JOIN INSTANCIA_ITEM ii4 ON ie.slot_armadura_escudo = ii4.id_instancia
            LEFT JOIN ITEM i4 ON ii4.id_item = i4.id_item
        """
        
        if classe == 'Espiritualista':
            query_base += """,
                e.slot_artefato,
                i5.nome as nome_artefato
            """
            joins_base += """
                LEFT JOIN ESPIRITUALISTA e ON ie.id_personagem = e.id_personagem
                LEFT JOIN INSTANCIA_ITEM ii5 ON e.slot_artefato = ii5.id_instancia
                LEFT JOIN ITEM i5 ON ii5.id_item = i5.id_item
            """
        elif classe == 'Titan':
            query_base += """,
                t.slot_extra_arma_1,
                t.slot_extra_arma_2,
                i5.nome as nome_arma_extra_1,
                i6.nome as nome_arma_extra_2
            """
            joins_base += """
                LEFT JOIN TITAN t ON ie.id_personagem = t.id_personagem
                LEFT JOIN INSTANCIA_ITEM ii5 ON t.slot_extra_arma_1 = ii5.id_instancia
                LEFT JOIN ITEM i5 ON ii5.id_item = i5.id_item
                LEFT JOIN INSTANCIA_ITEM ii6 ON t.slot_extra_arma_2 = ii6.id_instancia
                LEFT JOIN ITEM i6 ON ii6.id_item = i6.id_item
            """
        
        # Query completa
        query_completa = query_base + joins_base + " WHERE ie.id_personagem = %s;"
        
        cursor.execute(query_completa, (id_personagem,))
        resultado = cursor.fetchone()
        
        if resultado:
            resultado = dict(resultado)
            resultado['classe'] = classe
        
        return resultado
        
    except Exception as e:
        return None
    finally:
        cursor.close()

def menu_equipados_pygame(id_personagem):
    menu = MenuPyGame(title="Albion Online - Itens Equipados")
    
    while True:
        # Obter itens equipados
        equipados = obter_itens_equipados(id_personagem)
        
        # Obter classe do personagem
        classe = equipados.get('classe', 'Desconhecido') if equipados else obter_classe_personagem(id_personagem)
        
        # Mesmo se não há itens equipados, vamos mostrar os slots vazios
        if not equipados:
            # Criar um dicionário vazio para representar slots vazios
            equipados = {
                'slot_arma': None,
                'slot_armadura_capacete': None,
                'slot_armadura_peitoral': None,
                'slot_armadura_escudo': None,
                'nome_arma': None,
                'nome_armadura_capacete': None,
                'nome_armadura_peitoral': None,
                'nome_armadura_escudo': None,
                'classe': classe
            }
        
        # Preparar opções do menu com formato de boxes
        opcoes_menu = []
        slots_disponiveis = []
        
        # Slot de Arma Principal
        if equipados.get('slot_arma') and equipados.get('nome_arma'):
            opcoes_menu.append(f"⚔️ ARMA\n   {equipados['nome_arma']}")
            slots_disponiveis.append(('arma', equipados['slot_arma']))
        else:
            opcoes_menu.append(f"⚔️ ARMA\n   Slot Vazio")
            slots_disponiveis.append(None)
        
        # Slot de Armadura Peitoral
        if equipados.get('slot_armadura_peitoral') and equipados.get('nome_armadura_peitoral'):
            opcoes_menu.append(f"�️ PEITORAL\n   {equipados['nome_armadura_peitoral']}")
            slots_disponiveis.append(('armadura_peitoral', equipados['slot_armadura_peitoral']))
        else:
            opcoes_menu.append(f"�️ PEITORAL\n   Slot Vazio")
            slots_disponiveis.append(None)
        
        # Slot de Armadura Capacete
        if equipados.get('slot_armadura_capacete') and equipados.get('nome_armadura_capacete'):
            opcoes_menu.append(f"⛑️ CAPACETE\n   {equipados['nome_armadura_capacete']}")
            slots_disponiveis.append(('armadura_capacete', equipados['slot_armadura_capacete']))
        else:
            opcoes_menu.append(f"⛑️ CAPACETE\n   Slot Vazio")
            slots_disponiveis.append(None)
        
        # Slot de Armadura Escudo
        if equipados.get('slot_armadura_escudo') and equipados.get('nome_armadura_escudo'):
            opcoes_menu.append(f"🛡️ ESCUDO\n   {equipados['nome_armadura_escudo']}")
            slots_disponiveis.append(('armadura_escudo', equipados['slot_armadura_escudo']))
        else:
            opcoes_menu.append(f"🛡️ ESCUDO\n   Slot Vazio")
            slots_disponiveis.append(None)
        
        # Slots específicos por classe
        if classe == 'Espiritualista':
            # Slot de Artefato (apenas espiritualista)
            if equipados.get('slot_artefato') and equipados.get('nome_artefato'):
                opcoes_menu.append(f"✨ ARTEFATO\n   {equipados['nome_artefato']}")
                slots_disponiveis.append(('artefato', equipados['slot_artefato']))
            else:
                opcoes_menu.append(f"✨ ARTEFATO\n   Slot Vazio")
                slots_disponiveis.append(None)
                
        elif classe == 'Titan':
            # Slots extras de arma (apenas titan)
            if equipados.get('slot_extra_arma_1') and equipados.get('nome_arma_extra_1'):
                opcoes_menu.append(f"⚔️ ARMA EXTRA 1\n   {equipados['nome_arma_extra_1']}")
                slots_disponiveis.append(('arma_extra_1', equipados['slot_extra_arma_1']))
            else:
                opcoes_menu.append(f"⚔️ ARMA EXTRA 1\n   Slot Vazio")
                slots_disponiveis.append(None)
                
            if equipados.get('slot_extra_arma_2') and equipados.get('nome_arma_extra_2'):
                opcoes_menu.append(f"⚔️ ARMA EXTRA 2\n   {equipados['nome_arma_extra_2']}")
                slots_disponiveis.append(('arma_extra_2', equipados['slot_extra_arma_2']))
            else:
                opcoes_menu.append(f"⚔️ ARMA EXTRA 2\n   Slot Vazio")
                slots_disponiveis.append(None)
        
        opcoes_menu.append("🔙 Voltar")
        
        # Mostrar menu
        item_selecionado = menu.set_menu(
            title=f"ITENS EQUIPADOS - {classe}",
            options=opcoes_menu,
            subtitle="Selecione um slot para visualizar:"
        )
        
        # Verificar se usuário cancelou ou escolheu voltar
        if item_selecionado == -1 or item_selecionado == len(opcoes_menu) - 1:
            return "voltar"
        
        # Verificar se o slot selecionado tem item
        slot_info = slots_disponiveis[item_selecionado]
        
        if slot_info is None:
            menu.feedback("Slot Vazio", "Nenhum item equipado neste slot.", 2000)
            continue
        
        # Visualizar atributos do item equipado
        tipo_slot, id_instancia = slot_info
        item_info, tipo_item = visualizar_atributos_item(id_instancia)
        
        if item_info:
            atributos_formatados = formatar_atributos_item(item_info, tipo_item)
            
            # Mostrar atributos e opções de ação usando menu sem moldura
            opcoes_item = ["Desequipar Item", "🔙 Voltar aos Equipados"]
            
            acao_item = menu.set_menu(
                title="ATRIBUTOS DO ITEM EQUIPADO",
                options=opcoes_item,
                subtitle=atributos_formatados
            )
            
            if acao_item == 0:  # Desequipar Item
                # Confirmar desequipamento
                confirmacao = menu.set_menu(
                    title="CONFIRMAR DESEQUIPAMENTO",
                    options=["Sim, desequipar", "Cancelar"],
                    subtitle=f"Tem certeza que deseja desequipar este item?"
                )
                
                if confirmacao == 0:  # Confirmar desequipamento
                    from operadores.Inventario.desequipar_item import desequipar_item_slot_especifico, detectar_slot_do_item
                    
                    # Detectar o tipo de slot automaticamente
                    slot_tipo = detectar_slot_do_item(id_personagem, id_instancia)
                    
                    if not slot_tipo:
                        menu.feedback("Erro", "Não foi possível detectar o slot do item.", 3000)
                        continue
                    
                    cursor = criar_cursor()
                    try:
                        desequipar_item_slot_especifico(cursor, id_personagem, id_instancia, slot_tipo)
                        menu.feedback("Sucesso", "Item desequipado e movido para o inventário!", 2000)
                    except Exception as e:
                        menu.feedback("Erro", f"Erro ao desequipar item:\n{str(e)}", 3000)
                    finally:
                        cursor.close()
        else:
            menu.feedback("Erro", f"Não foi possível carregar os atributos do item.\n{tipo_item}", 3000)
