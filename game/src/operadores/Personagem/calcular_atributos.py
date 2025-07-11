from database import criar_cursor

def calcular_ataque_total_personagem(id_personagem):
    """
    Calcula o ataque físico total do personagem incluindo equipamentos
    Para Titans, inclui as armas extras
    """
    cursor = criar_cursor()
    try:
        # Verificar se é Titan
        cursor.execute("SELECT 1 FROM TITAN WHERE id_personagem = %s", (id_personagem,))
        eh_titan = cursor.fetchone() is not None
        
        if eh_titan:
            # Usar função específica para Titans
            cursor.execute("SELECT f_calcular_ataque_total_titan(%s) as ataque_total", (id_personagem,))
            resultado = cursor.fetchone()
            return resultado['ataque_total']
        else:
            # Para não-Titans, calcular ataque base + arma principal
            cursor.execute("""
                SELECT 
                    p.ataque_fisico as ataque_base,
                    COALESCE(a.aumento_ataque_fisico, 0) as bonus_arma
                FROM PERSONAGEM p
                LEFT JOIN INVENTARIO_EQUIPADOS ie ON p.id_personagem = ie.id_personagem
                LEFT JOIN INSTANCIA_ITEM ii ON ie.slot_arma = ii.id_instancia
                LEFT JOIN ITEM i ON ii.id_item = i.id_item
                LEFT JOIN EQUIPAVEL e ON i.id_item = e.id_item
                LEFT JOIN ARMA a ON e.id_item = a.id_item
                WHERE p.id_personagem = %s
            """, (id_personagem,))
            
            resultado = cursor.fetchone()
            if resultado:
                return resultado['ataque_base'] + resultado['bonus_arma']
            else:
                # Fallback: apenas ataque base
                cursor.execute("SELECT ataque_fisico FROM PERSONAGEM WHERE id_personagem = %s", (id_personagem,))
                personagem = cursor.fetchone()
                return personagem['ataque_fisico'] if personagem else 0
    
    except Exception as e:
        print(f"Erro ao calcular ataque total: {e}")
        # Fallback em caso de erro
        cursor.execute("SELECT ataque_fisico FROM PERSONAGEM WHERE id_personagem = %s", (id_personagem,))
        personagem = cursor.fetchone()
        return personagem['ataque_fisico'] if personagem else 0
    finally:
        cursor.connection.close()

def calcular_atributos_totais_personagem(id_personagem):
    """
    Calcula todos os atributos do personagem incluindo equipamentos
    Retorna um dicionário com os atributos totais
    """
    cursor = criar_cursor()
    try:
        # Obter atributos base
        cursor.execute("""
            SELECT vida_atual, vida_maxima, ataque_fisico, defesa_fisica, defesa_magica,
                   stamina_atual, stamina_maxima, nivel, exp_atual, exp_maxima, nome
            FROM PERSONAGEM 
            WHERE id_personagem = %s
        """, (id_personagem,))
        
        personagem = cursor.fetchone()
        if not personagem:
            return None
        
        # Calcular ataque total (incluindo equipamentos)
        ataque_total = calcular_ataque_total_personagem(id_personagem)
        
        # Calcular defesa e vida com equipamentos (armaduras e artefatos)
        cursor.execute("""
            SELECT 
                COALESCE(SUM(arm.aumento_defesa_fisica), 0) as bonus_def_fisica,
                COALESCE(SUM(arm.aumento_defesa_magica), 0) as bonus_def_magica,
                COALESCE(SUM(arm.aumento_vida_maxima), 0) as bonus_vida_maxima
            FROM INVENTARIO_EQUIPADOS ie
            LEFT JOIN INSTANCIA_ITEM ii_peitoral ON ie.slot_armadura_peitoral = ii_peitoral.id_instancia
            LEFT JOIN INSTANCIA_ITEM ii_capacete ON ie.slot_armadura_capacete = ii_capacete.id_instancia
            LEFT JOIN INSTANCIA_ITEM ii_escudo ON ie.slot_armadura_escudo = ii_escudo.id_instancia
            LEFT JOIN ITEM i_peitoral ON ii_peitoral.id_item = i_peitoral.id_item
            LEFT JOIN ITEM i_capacete ON ii_capacete.id_item = i_capacete.id_item
            LEFT JOIN ITEM i_escudo ON ii_escudo.id_item = i_escudo.id_item
            LEFT JOIN EQUIPAVEL e_peitoral ON i_peitoral.id_item = e_peitoral.id_item
            LEFT JOIN EQUIPAVEL e_capacete ON i_capacete.id_item = e_capacete.id_item
            LEFT JOIN EQUIPAVEL e_escudo ON i_escudo.id_item = e_escudo.id_item
            LEFT JOIN ARMADURA arm_peitoral ON e_peitoral.id_item = arm_peitoral.id_item
            LEFT JOIN ARMADURA arm_capacete ON e_capacete.id_item = arm_capacete.id_item
            LEFT JOIN ARMADURA arm_escudo ON e_escudo.id_item = arm_escudo.id_item
            LEFT JOIN ARMADURA arm ON arm.id_item IN (arm_peitoral.id_item, arm_capacete.id_item, arm_escudo.id_item)
            WHERE ie.id_personagem = %s
        """, (id_personagem,))
        
        bonus_armadura = cursor.fetchone()
        
        # Montar resultado final
        resultado = dict(personagem)
        resultado['ataque_fisico'] = ataque_total
        
        if bonus_armadura:
            resultado['defesa_fisica'] += bonus_armadura['bonus_def_fisica']
            resultado['defesa_magica'] += bonus_armadura['bonus_def_magica']
            # Vida máxima com bônus (mas vida atual permanece a mesma)
            resultado['vida_maxima'] += bonus_armadura['bonus_vida_maxima']
        
        return resultado
        
    except Exception as e:
        print(f"Erro ao calcular atributos totais: {e}")
        return dict(personagem) if personagem else None
    finally:
        cursor.connection.close()

def atualizar_stats_personagem(id_personagem):
    """
    Função de utilidade para obter os stats atualizados do personagem
    Esta função deve ser usada após qualquer ação que possa alterar os atributos:
    - Transformação dracônica
    - Equipar/desequipar itens
    - Usar magias
    - Qualquer mudança no inventário
    
    Returns: dict com os atributos atualizados ou None em caso de erro
    """
    return calcular_atributos_totais_personagem(id_personagem)
