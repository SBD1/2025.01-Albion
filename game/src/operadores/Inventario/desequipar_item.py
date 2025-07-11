from database import criar_cursor

def desequipar_item_slot_especifico(cursor, id_personagem, id_instancia_item, slot_tipo):
    """
    Desequipa um item de um slot específico e adiciona de volta ao inventário normal
    slot_tipo: 'slot_arma', 'slot_extra_arma_1', 'slot_extra_arma_2', etc.
    """
    try:
        # Verificar se há espaço no inventário
        cursor.execute("""
            SELECT COUNT(*) as itens_atual, i.capacidade
            FROM INVENTARIO i
            LEFT JOIN INVENTARIO_ITENS ii ON i.id_personagem = ii.id_personagem
            WHERE i.id_personagem = %s
            GROUP BY i.capacidade
        """, (id_personagem,))
        
        resultado = cursor.fetchone()
        if resultado:
            itens_atual = resultado['itens_atual']
            capacidade = resultado['capacidade']
            if itens_atual >= capacidade:
                raise Exception("Inventário cheio! Não é possível desequipar o item.")
        
        # Desequipar do slot específico
        if slot_tipo == 'slot_arma':
            cursor.execute("""
                UPDATE INVENTARIO_EQUIPADOS 
                SET slot_arma = NULL 
                WHERE id_personagem = %s AND slot_arma = %s
            """, (id_personagem, id_instancia_item))
        elif slot_tipo == 'slot_armadura_peitoral':
            cursor.execute("""
                UPDATE INVENTARIO_EQUIPADOS 
                SET slot_armadura_peitoral = NULL 
                WHERE id_personagem = %s AND slot_armadura_peitoral = %s
            """, (id_personagem, id_instancia_item))
        elif slot_tipo == 'slot_armadura_capacete':
            cursor.execute("""
                UPDATE INVENTARIO_EQUIPADOS 
                SET slot_armadura_capacete = NULL 
                WHERE id_personagem = %s AND slot_armadura_capacete = %s
            """, (id_personagem, id_instancia_item))
        elif slot_tipo == 'slot_armadura_escudo':
            cursor.execute("""
                UPDATE INVENTARIO_EQUIPADOS 
                SET slot_armadura_escudo = NULL 
                WHERE id_personagem = %s AND slot_armadura_escudo = %s
            """, (id_personagem, id_instancia_item))
        elif slot_tipo == 'slot_artefato':
            cursor.execute("""
                UPDATE ESPIRITUALISTA 
                SET slot_artefato = NULL 
                WHERE id_personagem = %s AND slot_artefato = %s
            """, (id_personagem, id_instancia_item))
        elif slot_tipo == 'slot_extra_arma_1':
            cursor.execute("""
                UPDATE TITAN 
                SET slot_extra_arma_1 = NULL 
                WHERE id_personagem = %s AND slot_extra_arma_1 = %s
            """, (id_personagem, id_instancia_item))
        elif slot_tipo == 'slot_extra_arma_2':
            cursor.execute("""
                UPDATE TITAN 
                SET slot_extra_arma_2 = NULL 
                WHERE id_personagem = %s AND slot_extra_arma_2 = %s
            """, (id_personagem, id_instancia_item))
        else:
            raise Exception(f"Tipo de slot inválido: {slot_tipo}")
        
        # Adicionar item de volta ao inventário normal
        cursor.execute("""
            INSERT INTO INVENTARIO_ITENS (id_personagem, id_instancia)
            VALUES (%s, %s)
        """, (id_personagem, id_instancia_item))
        
        cursor.connection.commit()
        return True
    except Exception as e:
        cursor.connection.rollback()
        raise e

def detectar_slot_do_item(id_personagem, id_instancia_item):
    """
    Detecta em qual slot um item está equipado
    Retorna: slot_tipo ou None se não estiver equipado
    """
    cursor = criar_cursor()
    try:
        # Verificar slots na tabela INVENTARIO_EQUIPADOS
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN slot_arma = %s THEN 'slot_arma'
                    WHEN slot_armadura_peitoral = %s THEN 'slot_armadura_peitoral'
                    WHEN slot_armadura_capacete = %s THEN 'slot_armadura_capacete'
                    WHEN slot_armadura_escudo = %s THEN 'slot_armadura_escudo'
                    ELSE NULL
                END as slot_tipo
            FROM INVENTARIO_EQUIPADOS
            WHERE id_personagem = %s
        """, (id_instancia_item, id_instancia_item, id_instancia_item, id_instancia_item, id_personagem))
        
        resultado = cursor.fetchone()
        if resultado and resultado['slot_tipo']:
            return resultado['slot_tipo']
        
        # Verificar slot de artefato (Espiritualista)
        cursor.execute("""
            SELECT 'slot_artefato' as slot_tipo
            FROM ESPIRITUALISTA
            WHERE id_personagem = %s AND slot_artefato = %s
        """, (id_personagem, id_instancia_item))
        
        resultado = cursor.fetchone()
        if resultado:
            return resultado['slot_tipo']
        
        # Verificar slots extras de arma (Titan)
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN slot_extra_arma_1 = %s THEN 'slot_extra_arma_1'
                    WHEN slot_extra_arma_2 = %s THEN 'slot_extra_arma_2'
                    ELSE NULL
                END as slot_tipo
            FROM TITAN
            WHERE id_personagem = %s
        """, (id_instancia_item, id_instancia_item, id_personagem))
        
        resultado = cursor.fetchone()
        if resultado and resultado['slot_tipo']:
            return resultado['slot_tipo']
        
        return None
        
    finally:
        cursor.connection.close()

def desequipar_item(cursor, id_instancia_item):
    """Função original mantida para compatibilidade - agora usa o novo sistema"""
    try:
        # Detectar qual personagem possui este item e em qual slot
        cursor.execute("""
            SELECT ie.id_personagem
            FROM INVENTARIO_EQUIPADOS ie
            WHERE ie.slot_arma = %s 
               OR ie.slot_armadura_peitoral = %s 
               OR ie.slot_armadura_capacete = %s 
               OR ie.slot_armadura_escudo = %s
            UNION
            SELECT e.id_personagem
            FROM ESPIRITUALISTA e
            WHERE e.slot_artefato = %s
            UNION
            SELECT t.id_personagem
            FROM TITAN t
            WHERE t.slot_extra_arma_1 = %s 
               OR t.slot_extra_arma_2 = %s
        """, (id_instancia_item, id_instancia_item, id_instancia_item, id_instancia_item, 
              id_instancia_item, id_instancia_item, id_instancia_item))
        
        resultado = cursor.fetchone()
        if not resultado:
            raise Exception("Item não está equipado.")
        
        id_personagem = resultado['id_personagem']
        slot_tipo = detectar_slot_do_item(id_personagem, id_instancia_item)
        
        if not slot_tipo:
            raise Exception("Não foi possível detectar o slot do item.")
        
        desequipar_item_slot_especifico(cursor, id_personagem, id_instancia_item, slot_tipo)
        print("✅ Item desequipado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao desequipar item: {e}")
        raise e