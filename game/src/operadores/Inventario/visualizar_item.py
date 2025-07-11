from database import criar_cursor

def visualizar_atributos_item(id_instancia_item):
    cursor = criar_cursor()
    
    try:
        # Primeiro, determinar o tipo do item
        cursor.execute("SELECT f_get_tipo_item(%s) as tipo;", (id_instancia_item,))
        tipo_info = cursor.fetchone()
        
        if not tipo_info or not tipo_info['tipo']:
            return None, "Item não encontrado"
        
        tipo_item = tipo_info['tipo']
        
        # Chamar a função específica baseada no tipo
        if tipo_item == 'Arma':
            cursor.execute("SELECT * FROM f_get_info_arma(%s);", (id_instancia_item,))
            resultado = cursor.fetchone()
            return resultado, tipo_item
            
        elif tipo_item == 'Armadura':
            cursor.execute("SELECT * FROM f_get_info_armadura(%s);", (id_instancia_item,))
            resultado = cursor.fetchone()
            
            if not resultado:
                return None, "Erro ao obter informações da armadura"
            
            # Verificar se é um escudo baseado no nome
            if 'escudo' in resultado.get('nome_armadura', '').lower():
                return resultado, 'Escudo'
            else:
                return resultado, tipo_item
            
        elif tipo_item == 'Artefato':
            cursor.execute("SELECT * FROM f_get_info_artefato(%s);", (id_instancia_item,))
            resultado = cursor.fetchone()
            return resultado, tipo_item
            
        elif tipo_item == 'Comida':
            cursor.execute("SELECT * FROM f_get_info_comida(%s);", (id_instancia_item,))
            resultado = cursor.fetchone()
            return resultado, tipo_item
            
        elif tipo_item == 'Pocao':
            cursor.execute("SELECT * FROM f_get_info_pocao(%s);", (id_instancia_item,))
            resultado = cursor.fetchone()
            return resultado, tipo_item
            
        elif tipo_item == 'Nao-Equipavel':
            # Para outros itens não equipáveis, usar função SQL básica
            cursor.execute("SELECT * FROM f_get_info_item_basico(%s);", (id_instancia_item,))
            resultado = cursor.fetchone()
            return resultado, "Item Básico"
            
        else:
            # Para outros tipos de itens, usar função SQL básica
            cursor.execute("SELECT * FROM f_get_info_item_basico(%s);", (id_instancia_item,))
            resultado = cursor.fetchone()
            return resultado, "Item Básico"
            
    except Exception as e:
        return None, f"Erro ao obter informações do item: {str(e)}"
    finally:
        cursor.close()

def formatar_atributos_item(item_info, tipo_item):
    """Formata as informações do item para exibição"""
    if not item_info:
        return "Informações não disponíveis"
    
    if tipo_item == 'Arma':
        return f"""Nome: {item_info['nome_arma']}
Descrição: {item_info['descricao']}
Tipo: Arma

Atributos:
• Aumento de Ataque Físico: +{item_info['aumento_ataque_fisico']}"""
    
    elif tipo_item == 'Armadura':
        return f"""Nome: {item_info['nome_armadura']}
Descrição: {item_info['descricao']}
Tipo: Armadura

Atributos:
• Aumento de Defesa Física: +{item_info['aumento_defesa_fisica']}
• Aumento de Defesa Mágica: +{item_info['aumento_defesa_magica']}
• Aumento de Vida Máxima: +{item_info['aumento_vida_maxima']}"""
    
    elif tipo_item == 'Escudo':
        return f"""Nome: {item_info['nome_armadura']}
Descrição: {item_info['descricao']}
Tipo: Escudo

Atributos:
• Aumento de Defesa Física: +{item_info['aumento_defesa_fisica']}
• Aumento de Defesa Mágica: +{item_info['aumento_defesa_magica']}
• Aumento de Vida Máxima: +{item_info['aumento_vida_maxima']}"""
    
    elif tipo_item == 'Artefato':
        return f"""Nome: {item_info['nome_armadura']}
Descrição: {item_info['descricao']}
Tipo: Artefato

Atributos:
• Aumento de Ataque Mágico: +{item_info['aumento_ataque_magico']}
• Aumento de Mana Máxima: +{item_info['aumento_mana_maxima']}"""
    
    elif tipo_item == 'Comida':
        return f"""Nome: {item_info['nome']}
Descrição: {item_info['descricao']}
Tipo: Comida

Efeitos:
• Recupera Vida: +{item_info['aumento_vida_atual']}
• Recupera Stamina: +{item_info['aumento_stamina_atual']}"""
    
    elif tipo_item == 'Pocao':
        return f"""Nome: {item_info['nome']}
Descrição: {item_info['descricao']}
Tipo: Poção

Efeitos:
• Recupera Mana: +{item_info['aumento_mana_atual']}"""
    
    else:  # Item Básico ou outros tipos
        return f"""Nome: {item_info.get('nome', 'N/A')}
Descrição: {item_info.get('descricao', 'Sem descrição')}
Tipo: {tipo_item}

Este item não possui atributos especiais."""
