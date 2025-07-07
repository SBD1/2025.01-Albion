from game.src.database import criar_cursor
from simple_term_menu import TerminalMenu
from game.src.limpar_tela import limpar_tela
import time

def obter_info_draconico(id_personagem):
    cursor = criar_cursor()
    try:
        query = """
        SELECT d.turnos_maximo_dragao, d.turnos_recarga, d.custo_stamina, d.aumento_vida_atual, d.aumento_ataque_fisico, p.stamina_atual, p.stamina_maxima
        FROM DRACONICO d
        JOIN PERSONAGEM p ON d.id_personagem = p.id_personagem
        WHERE d.id_personagem = %s
        """
        cursor.execute(query, (id_personagem,))
        resultado = cursor.fetchone()
        cursor.connection.close()
        return resultado
    except Exception as e:
        print(f"Erro ao obter informações do dracônico: {e}")
        cursor.connection.close()
        return None

def menu_transformacao_draconico(id_personagem):
    info = obter_info_draconico(id_personagem)
    if not info:
        print("Erro: Personagem não é um dracônico ou não foi encontrado.")
        time.sleep(4)
        return None

    custo_stamina = info['custo_stamina']
    stamina_atual = info['stamina_atual']
    aumento_vida = info['aumento_vida_atual']
    aumento_ataque = info['aumento_ataque_fisico']

    limpar_tela()
    print("=== TRANSFORMAÇÃO DRACÔNICA ===")
    print(f"Stamina: {stamina_atual}/{info['stamina_maxima']}")
    print(f"Custo para transformar: {custo_stamina} stamina")
    print()
    opcoes = [f"Transformar-se em Dragão (+{aumento_vida} vida, +{aumento_ataque} ataque)", "Voltar"]
    menu = TerminalMenu(opcoes, title="Escolha sua ação:")
    escolha = menu.show()

    if escolha == 1:
        return None  # Voltar

    if stamina_atual < custo_stamina:
        limpar_tela()
        print(f"Stamina insuficiente! Você precisa de {custo_stamina} stamina.")
        print(f"Stamina atual: {stamina_atual}")
        time.sleep(4)
        return None

    # Aplica transformação (exemplo: aumenta vida e ataque)
    cursor = criar_cursor()
    try:
        cursor.execute(
            "UPDATE PERSONAGEM SET vida_atual = vida_atual + %s, ataque_fisico = ataque_fisico + %s, stamina_atual = stamina_atual - %s WHERE id_personagem = %s;",
            (aumento_vida, aumento_ataque, custo_stamina, id_personagem)
        )
        cursor.connection.commit()
        cursor.connection.close()
        limpar_tela()
        print(f"🔥 Você se transformou em Dragão! (+{aumento_vida} vida, +{aumento_ataque} ataque)")
        time.sleep(3)
        return True
    except Exception as e:
        print(f"Erro ao transformar: {e}")
        cursor.connection.close()
        time.sleep(3)
        return None
