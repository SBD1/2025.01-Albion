from database import criar_cursor

def aplicar_xp(id_personagem: int, xp_ganho: int):
    cursor = criar_cursor()
    msgs = []
    
    # Obter dados atuais do personagem
    cursor.execute(
        "SELECT exp_atual, exp_maxima, nivel FROM public.personagem WHERE id_personagem = %s;",
        (id_personagem,)
    )
    p = cursor.fetchone()
    
    # Calcular novo XP e verificar se upou
    novo_xp_p = p['exp_atual'] + xp_ganho
    nivel_atual = p['nivel']
    niveis_ganhos = 0
    
    # Verificar quantos níveis foram ganhos
    while novo_xp_p >= p['exp_maxima']:
        novo_xp_p = novo_xp_p - p['exp_maxima']
        niveis_ganhos += 1
        # Atualizar exp_maxima para o próximo nível
        p['exp_maxima'] += 50
    
    # Atualizar XP e nível (trigger cuidará dos atributos)
    if niveis_ganhos > 0:
        cursor.execute(
            "UPDATE public.personagem SET exp_atual = %s, nivel = %s WHERE id_personagem = %s;",
            (novo_xp_p, nivel_atual + niveis_ganhos, id_personagem)
        )
        msgs.append("\n===================================\n  \033[1;32mPARABÉNS!\033[0m Você SUBIU DE NÍVEL!\n  Novos atributos, vida, stamina e XP máxima aumentados!\n  Vida, stamina e mana restaurados!\n===================================\n")
    else:
        cursor.execute(
            "UPDATE public.personagem SET exp_atual = %s WHERE id_personagem = %s;",
            (novo_xp_p, id_personagem)
        )
    
    msgs.append(f"Você ganhou {xp_ganho} pontos de EXP.")
    
    # Se for Zoiudo, atualizar XP do fantasma
    cursor.execute(
        "SELECT Z.id_fantasma FROM public.zoiudo Z WHERE Z.id_personagem = %s;",
        (id_personagem,)
    )
    zoiudo = cursor.fetchone()
    
    if zoiudo:
        id_fantasma = zoiudo['id_fantasma']
        
        # Obter dados atuais do fantasma
        cursor.execute(
            "SELECT exp_atual, exp_maxima, nivel FROM public.fantasma WHERE id_fantasma = %s;",
            (id_fantasma,)
        )
        f = cursor.fetchone()
        
        # Calcular novo XP e verificar se upou
        novo_xp_f = f['exp_atual'] + xp_ganho
        nivel_atual_f = f['nivel']
        niveis_ganhos_f = 0
        
        # Verificar quantos níveis foram ganhos
        while novo_xp_f >= f['exp_maxima']:
            novo_xp_f = novo_xp_f - f['exp_maxima']
            niveis_ganhos_f += 1
            # Atualizar exp_maxima para o próximo nível
            f['exp_maxima'] += 50
        
        # Atualizar XP e nível (trigger cuidará dos atributos)
        if niveis_ganhos_f > 0:
            cursor.execute(
                "UPDATE public.fantasma SET exp_atual = %s, nivel = %s WHERE id_fantasma = %s;",
                (novo_xp_f, nivel_atual_f + niveis_ganhos_f, id_fantasma)
            )
            msgs.append("\n==================================\n  \033[1;36mO FANTASMA SUBIU DE NÍVEL!\033[0m\n  Novos atributos, vida e XP máxima aumentados!\n  Vida restaurada!\n==================================\n")
        else:
            cursor.execute(
                "UPDATE public.fantasma SET exp_atual = %s WHERE id_fantasma = %s;",
                (novo_xp_f, id_fantasma)
            )
    
    cursor.connection.commit()
    cursor.connection.close()
    return msgs
