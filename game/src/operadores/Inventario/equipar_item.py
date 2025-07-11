from database import criar_cursor

def verificar_se_titan(id_personagem):
    """Verifica se o personagem é um Titan"""
    cursor = criar_cursor()
    try:
        cursor.execute("SELECT 1 FROM TITAN WHERE id_personagem = %s", (id_personagem,))
        return cursor.fetchone() is not None
    finally:
        cursor.connection.close()

def verificar_tipo_item(id_instancia_item):
    """Verifica o tipo de um item equipável"""
    cursor = criar_cursor()
    try:
        cursor.execute("""
            SELECT e.tipo_equipavel
            FROM INSTANCIA_ITEM ii
            JOIN ITEM i ON ii.id_item = i.id_item
            JOIN EQUIPAVEL e ON i.id_item = e.id_item
            WHERE ii.id_instancia = %s AND i.tipo_item = 'Equipavel'
        """, (id_instancia_item,))
        result = cursor.fetchone()
        return result['tipo_equipavel'] if result else None
    finally:
        cursor.connection.close()

def equipar_item_slot_especifico(cursor, id_personagem, id_instancia_item, slot_tipo):
    """
    Equipa um item em um slot específico
    slot_tipo: 'slot_arma', 'slot_extra_arma_1', 'slot_extra_arma_2', etc.
    """
    try:
        # Verificar se o item está no inventário do personagem
        cursor.execute("""
            SELECT 1 FROM INVENTARIO_ITENS 
            WHERE id_personagem = %s AND id_instancia = %s
        """, (id_personagem, id_instancia_item))
        
        if not cursor.fetchone():
            raise Exception("Item não encontrado no inventário.")
        
        # Verificar se há espaço no inventário para o item que será substituído 
        cursor.execute("""
            SELECT COUNT(*) as itens_atual, i.capacidade
            FROM INVENTARIO i
            LEFT JOIN INVENTARIO_ITENS ii ON i.id_personagem = ii.id_personagem
            WHERE i.id_personagem = %s
            GROUP BY i.capacidade
        """, (id_personagem,))
        
        resultado = cursor.fetchone()
        itens_atual = resultado['itens_atual'] if resultado else 0
        capacidade = resultado['capacidade'] if resultado else 10
        
        # Verificar se há item já equipado no slot e mover para inventário
        item_anterior = None
        
        if slot_tipo == 'slot_arma':
            # Verificar slot padrão na tabela INVENTARIO_EQUIPADOS
            cursor.execute("""
                SELECT slot_arma FROM INVENTARIO_EQUIPADOS 
                WHERE id_personagem = %s AND slot_arma IS NOT NULL
            """, (id_personagem,))
            resultado_anterior = cursor.fetchone()
            if resultado_anterior:
                item_anterior = resultado_anterior['slot_arma']
                
        elif slot_tipo in ['slot_extra_arma_1', 'slot_extra_arma_2']:
            # Verificar slots extras na tabela TITAN
            cursor.execute(f"""
                SELECT {slot_tipo} FROM TITAN 
                WHERE id_personagem = %s AND {slot_tipo} IS NOT NULL
            """, (id_personagem,))
            resultado_anterior = cursor.fetchone()
            if resultado_anterior:
                item_anterior = resultado_anterior[slot_tipo]
        
        # Se há item anterior e não há espaço no inventário, cancelar operação
        if item_anterior and itens_atual >= capacidade:
            raise Exception("Inventário cheio! Não é possível substituir o item equipado.")
        
        # Mover item anterior para inventário 
        if item_anterior:
            cursor.execute("""
                INSERT INTO INVENTARIO_ITENS (id_personagem, id_instancia)
                VALUES (%s, %s)
            """, (id_personagem, item_anterior))
        
        # Equipar novo item no slot
        if slot_tipo == 'slot_arma':
            # Slot padrão na tabela INVENTARIO_EQUIPADOS
            cursor.execute(
                "INSERT INTO INVENTARIO_EQUIPADOS (id_personagem, slot_arma) VALUES (%s, %s) "
                "ON CONFLICT (id_personagem) DO UPDATE SET slot_arma = %s",
                (id_personagem, id_instancia_item, id_instancia_item)
            )
        elif slot_tipo in ['slot_extra_arma_1', 'slot_extra_arma_2']:
            # Slots extras na tabela TITAN
            cursor.execute(f"""
                UPDATE TITAN 
                SET {slot_tipo} = %s 
                WHERE id_personagem = %s
            """, (id_instancia_item, id_personagem))
        else:
            raise Exception(f"Tipo de slot inválido: {slot_tipo}")
        
        # Remover novo item do inventário normal após equipar
        cursor.execute("""
            DELETE FROM INVENTARIO_ITENS 
            WHERE id_personagem = %s AND id_instancia = %s
        """, (id_personagem, id_instancia_item))
        
        cursor.connection.commit()
        return True
    except Exception as e:
        cursor.connection.rollback()
        raise e

def equipar_item(cursor, id_instancia_item):
    """Função original atualizada para tratar substituição de itens e remoção do inventário"""
    try:
        # Obter informações do item e personagem
        cursor.execute("""
            SELECT inv.id_personagem, ii.id_item, e.tipo_equipavel, i.nome
            FROM INVENTARIO_ITENS inv
            JOIN INSTANCIA_ITEM ii ON inv.id_instancia = ii.id_instancia
            JOIN ITEM i ON ii.id_item = i.id_item
            JOIN EQUIPAVEL e ON i.id_item = e.id_item
            WHERE inv.id_instancia = %s
        """, (id_instancia_item,))
        
        resultado = cursor.fetchone()
        if not resultado:
            raise Exception("Item não encontrado no inventário ou não é equipável.")
        
        id_personagem = resultado['id_personagem']
        tipo_equipavel = resultado['tipo_equipavel']
        nome_item = resultado['nome']
        
        # Verificar capacidade do inventário
        cursor.execute("""
            SELECT COUNT(*) as itens_atual, i.capacidade
            FROM INVENTARIO i
            LEFT JOIN INVENTARIO_ITENS ii ON i.id_personagem = ii.id_personagem
            WHERE i.id_personagem = %s
            GROUP BY i.capacidade
        """, (id_personagem,))
        
        resultado_inv = cursor.fetchone()
        itens_atual = resultado_inv['itens_atual'] if resultado_inv else 0
        capacidade = resultado_inv['capacidade'] if resultado_inv else 10
        
        # Determinar slot e verificar item anterior
        item_anterior = None
        slot_info = ""
        
        if tipo_equipavel == 'Arma':
            # Verificar item na slot_arma
            cursor.execute("""
                SELECT slot_arma FROM INVENTARIO_EQUIPADOS 
                WHERE id_personagem = %s AND slot_arma IS NOT NULL
            """, (id_personagem,))
            resultado_anterior = cursor.fetchone()
            if resultado_anterior:
                item_anterior = resultado_anterior['slot_arma']
            slot_info = "slot_arma"
            
        elif tipo_equipavel == 'Armadura':
            # Determinar tipo específico de armadura pelo nome
            if 'Peitoral' in nome_item:
                cursor.execute("""
                    SELECT slot_armadura_peitoral FROM INVENTARIO_EQUIPADOS 
                    WHERE id_personagem = %s AND slot_armadura_peitoral IS NOT NULL
                """, (id_personagem,))
                resultado_anterior = cursor.fetchone()
                if resultado_anterior:
                    item_anterior = resultado_anterior['slot_armadura_peitoral']
                slot_info = "slot_armadura_peitoral"
                
            elif 'Capacete' in nome_item:
                cursor.execute("""
                    SELECT slot_armadura_capacete FROM INVENTARIO_EQUIPADOS 
                    WHERE id_personagem = %s AND slot_armadura_capacete IS NOT NULL
                """, (id_personagem,))
                resultado_anterior = cursor.fetchone()
                if resultado_anterior:
                    item_anterior = resultado_anterior['slot_armadura_capacete']
                slot_info = "slot_armadura_capacete"
                
            elif 'Escudo' in nome_item:
                cursor.execute("""
                    SELECT slot_armadura_escudo FROM INVENTARIO_EQUIPADOS 
                    WHERE id_personagem = %s AND slot_armadura_escudo IS NOT NULL
                """, (id_personagem,))
                resultado_anterior = cursor.fetchone()
                if resultado_anterior:
                    item_anterior = resultado_anterior['slot_armadura_escudo']
                slot_info = "slot_armadura_escudo"
                
        elif tipo_equipavel == 'Artefato':
            # Verificar se é espiritualista
            cursor.execute("""
                SELECT slot_artefato FROM ESPIRITUALISTA 
                WHERE id_personagem = %s AND slot_artefato IS NOT NULL
            """, (id_personagem,))
            resultado_anterior = cursor.fetchone()
            if resultado_anterior:
                item_anterior = resultado_anterior['slot_artefato']
            slot_info = "slot_artefato"
        
        # Se há item anterior e não há espaço, cancelar
        if item_anterior and itens_atual >= capacidade:
            raise Exception("Inventário cheio! Não é possível substituir o item equipado.")
        
        # Mover item anterior para inventário (se existir)
        if item_anterior:
            cursor.execute("""
                INSERT INTO INVENTARIO_ITENS (id_personagem, id_instancia)
                VALUES (%s, %s)
            """, (id_personagem, item_anterior))
        
        # Equipar usando a função SQL original
        cursor.execute(f"SELECT f_equipar_item({id_instancia_item});")
        
        # Remover novo item do inventário normal após equipar
        cursor.execute("""
            DELETE FROM INVENTARIO_ITENS 
            WHERE id_personagem = %s AND id_instancia = %s
        """, (id_personagem, id_instancia_item))
        
        cursor.connection.commit()
        print("✅ Item equipado com sucesso!")
    except Exception as e:
        cursor.connection.rollback()
        print(f"❌ Erro ao equipar item: {e}")
        raise e