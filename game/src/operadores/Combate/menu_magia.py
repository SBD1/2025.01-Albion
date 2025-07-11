from database import criar_cursor
from operadores.Menus.estrutura_menu_pygame import MenuPyGame
import math

def calcular_dano_magico(ataque_magico: int, defesa_magica: int, fator: int = 100) -> int:
    """
    Fórmula de dano mágico: ataque_magico * fator / (defesa_magica + fator)
    Mitigação percentual inspirada em Elder Scrolls.
    Garante retorno decrescente sem zerar o dano (mínimo 1).
    """
    if defesa_magica < 0:
        defesa_magica = 0
    proporcao = ataque_magico * fator / (defesa_magica + fator)
    return max(1, math.floor(proporcao))

def obter_info_espiritualista(id_personagem):
    """Obtém informações do personagem espiritualista"""
    cursor = criar_cursor()
    try:
        query = (
            "SELECT p.nivel, p.nome, e.mana_atual, e.mana_total, e.ataque_magico "
            "FROM PERSONAGEM p JOIN ESPIRITUALISTA e ON p.id_personagem = e.id_personagem "
            "WHERE p.id_personagem = %s"
        )
        cursor.execute(query, (id_personagem,))
        resultado = cursor.fetchone()
        cursor.connection.close()
        return resultado
    except Exception as e:
        print(f"Erro ao obter informações do espiritualista: {e}")
        cursor.connection.close()
        return None

def obter_magias_disponiveis(nivel_personagem):
    """Obtém todas as magias que o personagem pode usar baseado no nível"""
    cursor = criar_cursor()
    try:
        query = (
            "SELECT id_magia, nome, descricao, nivel_requerido, custo_mana, dano_base, cura_base "
            "FROM public.MAGIA WHERE nivel_requerido <= %s "
            "ORDER BY nivel_requerido ASC, nome ASC"
        )
        cursor.execute(query, (nivel_personagem,))
        magias = cursor.fetchall()
        return magias
    except Exception as e:
        menu = MenuPyGame()
        print(f"Erro ao obter magias: {e}")
        return []
    finally:
        if cursor and hasattr(cursor, 'connection'):
            cursor.connection.close()

def usar_magia(id_personagem, id_instancia, defesa_magica_monstro, vida_atual_monstro):
    """Menu principal para usar magias"""
    menu = MenuPyGame()
    # Obtém informações do espiritualista
    info_espiritualista = obter_info_espiritualista(id_personagem)
    if not info_espiritualista:
        print("Erro: Personagem não é um espiritualista ou não foi encontrado.")
        return None, None
    nivel = info_espiritualista['nivel']
    nome = info_espiritualista['nome']
    mana_atual = info_espiritualista['mana_atual']
    mana_total = info_espiritualista['mana_total']
    ataque_magico = info_espiritualista['ataque_magico']
    
    # Obtém magias disponíveis
    magias_disponiveis = obter_magias_disponiveis(nivel)
    
    if not magias_disponiveis:
        menu = MenuPyGame()
        menu.feedback(
            "MAGIA",
            f"Nenhuma magia disponível para seu nível atual.\nNível: {nivel}",
            duration=3000
        )
        return None, None
    
    while True:
        # Menu de seleção de magia
        subtitle = f"Espiritualista: {nome} | Nível: {nivel}\nMana: {mana_atual}/{mana_total}"
        opcoes_menu = []
        magias_validas = []
        
        for magia in magias_disponiveis:
            # Verifica se tem mana suficiente
            pode_usar = mana_atual >= magia['custo_mana']
            status = "✓" if pode_usar else "✗"
            
            # Determina tipo da magia
            if magia['dano_base'] > 0 and magia['cura_base'] > 0:
                tipo = "Mista"
            elif magia['dano_base'] > 0:
                tipo = "Ofensiva"
            elif magia['cura_base'] > 0:
                tipo = "Cura"
            else:
                tipo = "Outras"
            
            opcao = f"{status} {magia['nome']} (Nv.{magia['nivel_requerido']}) - {tipo} - Custo: {magia['custo_mana']} mana"
            opcoes_menu.append(opcao)
            magias_validas.append(magia)
        
        opcoes_menu.append("Voltar")
        
        escolha = menu.set_menu("Escolha uma magia para conjurar:", opcoes_menu, subtitle=subtitle)
        
        if escolha == len(opcoes_menu) - 1:  # Voltar
            return None, None
        
        magia_escolhida = magias_validas[escolha]
        
        # Verifica se tem mana suficiente
        if mana_atual < magia_escolhida['custo_mana']:
            menu.feedback("MAGIA", f"Mana insuficiente! Necessário {magia_escolhida['custo_mana']} mana.\nMana atual: {mana_atual}", duration=3000)
            continue
        
        # Conjura a magia
        resultado = conjurar_magia(
            id_personagem, 
            magia_escolhida, 
            ataque_magico, 
            defesa_magica_monstro, 
            id_instancia, 
            vida_atual_monstro
        )
        
        if resultado:
            nova_mana, nova_vida_monstro = resultado
            return nova_mana, nova_vida_monstro
        else:
            continue

def conjurar_magia(id_personagem, magia, ataque_magico, defesa_magica_monstro, id_instancia, vida_atual_monstro):
    """Executa a lógica de conjurar uma magia"""
    
    cursor = criar_cursor()
    try:
        # Calcula dano baseado no ataque mágico do personagem e dano base da magia
        dano_final = 0
        cura_final = 0
        
        if magia['dano_base'] > 0:
            # Dano = (ataque_magico_personagem + dano_base_magia) vs defesa_magica_monstro
            ataque_total = ataque_magico + magia['dano_base']
            dano_final = calcular_dano_magico(ataque_total, defesa_magica_monstro)
        
        if magia['cura_base'] > 0:
            # Cura é direta (não há "defesa" contra cura)
            cura_final = magia['cura_base']
        
        # Consome mana
        cursor.execute(
            "UPDATE ESPIRITUALISTA SET mana_atual = mana_atual - %s WHERE id_personagem = %s",
            (magia['custo_mana'], id_personagem)
        )
        
        # Aplica dano ao monstro se houver
        nova_vida_monstro = vida_atual_monstro
        if dano_final > 0:
            nova_vida_monstro = max(0, vida_atual_monstro - dano_final)
            cursor.execute(
                "UPDATE INSTANCIA_NPC_GENERICO SET vida_atual = %s WHERE id_instancia = %s",
                (nova_vida_monstro, id_instancia)
            )
        
        # Aplica cura ao personagem se houver
        if cura_final > 0:
            cursor.execute(
                "UPDATE PERSONAGEM SET vida_atual = LEAST(vida_atual + %s, vida_maxima) WHERE id_personagem = %s",
                (cura_final, id_personagem)
            )
        
        # Obtém nova mana atual
        cursor.execute(
            "SELECT mana_atual FROM ESPIRITUALISTA WHERE id_personagem = %s",
            (id_personagem,)
        )
        nova_mana = cursor.fetchone()['mana_atual']
        
        cursor.connection.commit()
        cursor.connection.close()
        
        # Feedback via Pygame
        menu = MenuPyGame()
        details = []
        if dano_final > 0:
            details.append(f"Dano: {dano_final}")
        if cura_final > 0:
            details.append(f"Cura: {cura_final}")
        details.append(f"Mana consumida: {magia['custo_mana']}")
        details.append(f"Mana restante: {nova_mana}")
        texto = f"{magia['descricao']}\n" + "\n".join(details)
        menu.feedback(f"{magia['nome']}", texto, duration=5000)
        
        return nova_mana, nova_vida_monstro
        
    except Exception as e:
        print(f"Erro ao conjurar magia: {e}")
        cursor.connection.close()
        return None

def menu_magia(id_personagem, id_instancia, monstro_stats):
    """Função principal chamada pelo menu de combate, agora recebe stats do monstro"""
    return usar_magia(id_personagem, id_instancia, monstro_stats['defesa_magica'], monstro_stats['vida_atual'])