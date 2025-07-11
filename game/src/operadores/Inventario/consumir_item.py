from database import criar_cursor

def obter_info_consumivel(id_instancia_item):
    """
    Obtém informações sobre um item consumível (comida ou poção)
    Retorna: (tipo_consumivel, efeitos_dict) ou (None, None) se não for consumível
    """
    cursor = criar_cursor()
    try:
        # Verificar se é um item não-equipável
        cursor.execute("""
            SELECT i.nome, ne.tipo_nequipavel, i.id_item
            FROM INSTANCIA_ITEM ii
            JOIN ITEM i ON ii.id_item = i.id_item
            JOIN NEQUIPAVEL ne ON i.id_item = ne.id_item
            WHERE ii.id_instancia = %s AND i.tipo_item = 'Nao-Equipavel'
        """, (id_instancia_item,))
        
        item_info = cursor.fetchone()
        if not item_info:
            return None, None
        
        tipo_consumivel = item_info['tipo_nequipavel']
        id_item = item_info['id_item']
        nome_item = item_info['nome']
        
        # Buscar efeitos específicos baseado no tipo
        if tipo_consumivel == 'Comida':
            cursor.execute("""
                SELECT aumento_vida_atual, aumento_stamina_atual
                FROM COMIDA
                WHERE id_item = %s
            """, (id_item,))
            efeitos = cursor.fetchone()
            if efeitos:
                efeitos_dict = {
                    'vida': efeitos['aumento_vida_atual'],
                    'stamina': efeitos['aumento_stamina_atual'],
                    'nome': nome_item
                }
                return 'Comida', efeitos_dict
                
        elif tipo_consumivel == 'Pocao':
            cursor.execute("""
                SELECT aumento_mana_atual
                FROM POCAO
                WHERE id_item = %s
            """, (id_item,))
            efeitos = cursor.fetchone()
            if efeitos:
                efeitos_dict = {
                    'mana': efeitos['aumento_mana_atual'],
                    'nome': nome_item
                }
                return 'Pocao', efeitos_dict
        
        return None, None
        
    except Exception as e:
        print(f"Erro ao obter informações do consumível: {e}")
        return None, None
    finally:
        cursor.connection.close()

def consumir_item(id_personagem, id_instancia_item):
    """
    Consome um item (comida ou poção), aplicando seus efeitos e removendo do inventário
    Retorna: (sucesso: bool, mensagem: str)
    """
    # Primeiro, verificar se é consumível e obter efeitos
    tipo_consumivel, efeitos = obter_info_consumivel(id_instancia_item)
    
    if not tipo_consumivel or not efeitos:
        return False, "Este item não é consumível."
    
    cursor = criar_cursor()
    try:
        # Verificar se o item está no inventário do personagem
        cursor.execute("""
            SELECT 1 FROM INVENTARIO_ITENS 
            WHERE id_personagem = %s AND id_instancia = %s
        """, (id_personagem, id_instancia_item))
        
        if not cursor.fetchone():
            return False, "Item não encontrado no seu inventário."
        
        # Aplicar efeitos baseado no tipo
        if tipo_consumivel == 'Comida':
            # Atualizar vida e stamina (sem ultrapassar máximos)
            cursor.execute("""
                UPDATE PERSONAGEM 
                SET vida_atual = LEAST(vida_atual + %s, vida_maxima),
                    stamina_atual = LEAST(stamina_atual + %s, stamina_maxima)
                WHERE id_personagem = %s
            """, (efeitos['vida'], efeitos['stamina'], id_personagem))
            
            mensagem = f"Você consumiu {efeitos['nome']}! +{efeitos['vida']} vida, +{efeitos['stamina']} stamina."
            
        elif tipo_consumivel == 'Pocao':
            # Atualizar mana (verificar se é espiritualista)
            cursor.execute("""
                UPDATE ESPIRITUALISTA 
                SET mana_atual = LEAST(mana_atual + %s, mana_total)
                WHERE id_personagem = %s
            """, (efeitos['mana'], id_personagem))
            
            # Verificar se a atualização afetou alguma linha (se é espiritualista)
            if cursor.rowcount == 0:
                return False, "Apenas Espiritualistas podem usar poções de mana."
            
            mensagem = f"Você consumiu {efeitos['nome']}! +{efeitos['mana']} mana."
        
        # Remover item do inventário
        cursor.execute("""
            DELETE FROM INVENTARIO_ITENS 
            WHERE id_personagem = %s AND id_instancia = %s
        """, (id_personagem, id_instancia_item))
        
        # Remover instância do item
        cursor.execute("""
            DELETE FROM INSTANCIA_ITEM 
            WHERE id_instancia = %s
        """, (id_instancia_item,))
        
        cursor.connection.commit()
        return True, mensagem
        
    except Exception as e:
        cursor.connection.rollback()
        return False, f"Erro ao consumir item: {str(e)}"
    finally:
        cursor.connection.close()

def verificar_se_consumivel(id_instancia_item):
    """
    Verifica se um item é consumível
    Retorna: True se for consumível, False caso contrário
    """
    tipo, _ = obter_info_consumivel(id_instancia_item)
    return tipo is not None
