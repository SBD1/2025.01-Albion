from database import criar_cursor
from operadores.Menus.estrutura_menu_pygame import MenuPyGame

def obter_info_draconico(id_personagem):
    cursor = criar_cursor()
    try:
        query = """
        SELECT d.custo_stamina, d.aumento_vida_atual, d.aumento_ataque_fisico, p.stamina_atual, p.stamina_maxima
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
    menu = MenuPyGame()
    info = obter_info_draconico(id_personagem)
    if not info:
        print("Erro: Personagem não é um dracônico ou não foi encontrado.")
        return None

    # Custo é sempre metade da stamina máxima
    custo_stamina = info['stamina_maxima'] // 2
    stamina_atual = info['stamina_atual']
    aumento_vida = info['aumento_vida_atual']
    aumento_ataque = info['aumento_ataque_fisico']
    # Menu de transformação
    title = "TRANSFORMAÇÃO DRACÔNICA"
    subtitle = f"Stamina: {stamina_atual}/{info['stamina_maxima']}\nCusto: {custo_stamina} stamina"
    opcoes = [f"Transformar-se em Dragão (+{aumento_vida} vida, +{aumento_ataque} ataque)", "Voltar"]
    escolha = menu.set_menu(title, opcoes, subtitle=subtitle)

    if escolha == 1:
        return None  # Voltar

    if stamina_atual < custo_stamina:
        menu.feedback(
            "TRANSFORMAÇÃO",
            f"Stamina insuficiente! Custo: {custo_stamina}. Atual: {stamina_atual}",
            duration=3000
        )
        return None

    # Aplica transformação: desconta stamina e adiciona bônus
    cursor = criar_cursor()
    try:
        cursor.execute(
            "UPDATE PERSONAGEM SET stamina_atual = stamina_atual - %s, vida_atual = vida_atual + %s, ataque_fisico = ataque_fisico + %s WHERE id_personagem = %s;",
            (custo_stamina, aumento_vida, aumento_ataque, id_personagem)
        )
        cursor.connection.commit()
        cursor.connection.close()
        menu.feedback(
            "TRANSFORMAÇÃO",
            f"🔥 Transformado em Dragão! (+{aumento_vida} vida, +{aumento_ataque} ataque)",
            duration=3000
        )
        return True
    except Exception as e:
        menu.feedback("TRANSFORMAÇÃO", f"Erro ao transformar: {e}", duration=3000)
        return None

def iniciar_combate_draconico(id_personagem: int, id_instancia: int, monstro_stats: dict) -> str:
    """
    Loop de combate exclusivo para dracônico após transformação.
    Opções: Atacar, Cancelar Transformação.
    Retorna 'vitoria', 'cancel' ou 'derrota'.
    """
    menu = MenuPyGame()
    from operadores.Combate.logica_ataque import calcular_dano_fisico
    from database import criar_cursor
    
    # Buscar stats atualizados do personagem (já com bônus aplicados)
    cursor = criar_cursor()
    cursor.execute(
        "SELECT vida_atual, ataque_fisico, defesa_fisica FROM PERSONAGEM WHERE id_personagem = %s;",
        (id_personagem,)
    )
    p = cursor.fetchone()
    vida_atual = p['vida_atual']
    ataque_fisico = p['ataque_fisico']
    defesa_fisica = p['defesa_fisica']
    cursor.connection.close()

    vida_maxima_monstro = monstro_stats.get('vida_maxima', 1)
    defesa_fisica_monstro = monstro_stats.get('defesa_fisica', 0)
    vida_atual_monstro = monstro_stats.get('vida_atual', vida_maxima_monstro)
    npc_especie = monstro_stats.get('especie', 'Monstro')

    selected = 0
    while True:
        status_info = {
            'monstro': {'especie': npc_especie, 'vida_atual': vida_atual_monstro, 'vida_maxima': vida_maxima_monstro},
            'personagem': {'nome': 'Dracônico', 'vida_atual': vida_atual, 'vida_maxima': p.get('vida_maxima', vida_atual)}
        }

        opcoes = ['⚔️ Atacar', '❌ Cancelar Transformação']
        escolha = menu.set_menu_combate('🐉 Combate Dracônico 🐉', status_info, opcoes, selected)
        selected = escolha if escolha >= 0 else selected
        acao = opcoes[escolha] if escolha >= 0 else None

        if acao == '❌ Cancelar Transformação':
            # Reverte vida e ataque para valores originais antes da transformação
            cursor2 = criar_cursor()
            cursor2.execute(
                "SELECT aumento_vida_atual, aumento_ataque_fisico FROM public.DRACONICO WHERE id_personagem = %s;",
                (id_personagem,)
            )
            draco = cursor2.fetchone()
            bonus_vida = draco.get('aumento_vida_atual')
            bonus_ataque = draco.get('aumento_ataque_fisico')
            # Define vida igual ao bônus de vida e remove bônus de ataque
            cursor2.execute(
                "UPDATE public.PERSONAGEM SET vida_atual = %s, ataque_fisico = ataque_fisico - %s WHERE id_personagem = %s;",
                (bonus_vida, bonus_ataque, id_personagem)
            )
            cursor2.connection.commit()
            cursor2.connection.close()
            return 'cancel'

        # Atacar
        dano = calcular_dano_fisico(ataque_fisico, defesa_fisica_monstro)
        vida_atual_monstro = max(0, vida_atual_monstro - dano)
        # Atualiza vida do monstro
        cursor = criar_cursor()
        cursor.execute(
            "UPDATE INSTANCIA_NPC_GENERICO SET vida_atual = %s WHERE id_instancia = %s;",
            (vida_atual_monstro, id_instancia)
        )
        cursor.connection.commit()
        cursor.connection.close()
        menu.feedback('ATAQUE DRACÔNICO', f'Draco causou {dano} de dano!', duration=3000)

        if vida_atual_monstro <= 0:
            menu.feedback('VITÓRIA', f'{npc_especie} derrotado!', duration=3000)
            # Reverte bônus de transformação após vitória
            cursor2 = criar_cursor()
            cursor2.execute(
                "SELECT aumento_vida_atual, aumento_ataque_fisico FROM public.DRACONICO WHERE id_personagem = %s;",
                (id_personagem,)
            )
            draco = cursor2.fetchone()
            bonus_vida = draco.get('aumento_vida_atual')
            bonus_ataque = draco.get('aumento_ataque_fisico')
            cursor2.execute(
                "UPDATE public.PERSONAGEM SET vida_atual = %s, ataque_fisico = ataque_fisico - %s WHERE id_personagem = %s;",
                (bonus_vida, bonus_ataque, id_personagem)
            )
            cursor2.connection.commit()
            cursor2.connection.close()
            return 'vitoria'

        # Turno do monstro
        menu.feedback('TURNO INIMIGO', 'Monstro contra-ataca!', duration=3000)
        dmg = calcular_dano_fisico(monstro_stats.get('ataque_fisico',0), p['defesa_fisica'])
        vida_atual = max(0, vida_atual - dmg)
        cursor = criar_cursor()
        cursor.execute(
            "UPDATE PERSONAGEM SET vida_atual = %s WHERE id_personagem = %s;",
            (vida_atual, id_personagem)
        )
        cursor.connection.commit()
        cursor.connection.close()
        menu.feedback('DANO', f'Monstro causou {dmg} de dano!', duration=3000)

        if vida_atual <= 0:
            menu.feedback('DERROTA', 'Você morreu!', duration=3000)
            # Reverte bônus de transformação após derrota
            cursor2 = criar_cursor()
            cursor2.execute(
                "SELECT aumento_vida_atual, aumento_ataque_fisico FROM public.DRACONICO WHERE id_personagem = %s;",
                (id_personagem,)
            )
            draco = cursor2.fetchone()
            bonus_vida = draco.get('aumento_vida_atual')
            bonus_ataque = draco.get('aumento_ataque_fisico')
            cursor2.execute(
                "UPDATE public.PERSONAGEM SET ataque_fisico = ataque_fisico - %s WHERE id_personagem = %s;",
                (bonus_vida, bonus_ataque, id_personagem)
            )
            cursor2.connection.commit()
            cursor2.connection.close()
            return 'derrota'
        # continua loop para próximo ataque
