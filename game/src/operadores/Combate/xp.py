from game.src.database import criar_cursor

def aplicar_xp(id_personagem: int, xp_ganho: int):
    cursor = criar_cursor()
    msgs = []
    cursor.execute(
        "SELECT exp_atual, exp_maxima, ataque_fisico, defesa_fisica, defesa_magica, nivel, vida_maxima, stamina_maxima FROM public.personagem WHERE id_personagem = %s;",
        (id_personagem,)
    )
    p = cursor.fetchone()
    novo_xp_p = p['exp_atual'] + xp_ganho
    upou_p = False
    if novo_xp_p >= p['exp_maxima']:
        novo_xp_p = novo_xp_p - p['exp_maxima']
        upou_p = True
    cursor.execute(
        "UPDATE public.personagem SET exp_atual = %s WHERE id_personagem = %s;",
        (novo_xp_p, id_personagem)
    )
    if upou_p:
        cursor.execute(
            "UPDATE public.personagem SET ataque_fisico = ataque_fisico + 10, defesa_fisica = defesa_fisica + 10, defesa_magica = defesa_magica + 10, nivel = nivel + 1, exp_maxima = exp_maxima + 50, vida_maxima = vida_maxima + 20, stamina_maxima = stamina_maxima + 10 WHERE id_personagem = %s;",
            (id_personagem,)
        )
        cursor.execute(
            "UPDATE public.personagem SET vida_atual = vida_maxima, stamina_atual = stamina_maxima WHERE id_personagem = %s;",
            (id_personagem,)
        )
        cursor.execute(
            "UPDATE public.espiritualista SET mana_atual = mana_total WHERE id_personagem = %s;",
            (id_personagem,)
        )
        msgs.append("\n===================================\n  \033[1;32mPARABÉNS!\033[0m Você SUBIU DE NÍVEL!\n  Novos atributos, vida, stamina e XP máxima aumentados!\n  Vida, stamina e mana restaurados!\n===================================\n")
    msgs.append(f"Você ganhou {xp_ganho} pontos de EXP.")
    # Se for Zoiudo, atualiza XP do fantasma
    cursor.execute(
        "SELECT Z.id_fantasma FROM public.zoiudo Z WHERE Z.id_personagem = %s;",
        (id_personagem,)
    )
    zoiudo = cursor.fetchone()
    upou_f = False
    if zoiudo:
        id_fantasma = zoiudo['id_fantasma']
        cursor.execute(
            "SELECT exp_atual, exp_maxima, ataque_fisico, ataque_magico, defesa_fisica, defesa_magica, nivel, vida_maxima FROM public.fantasma WHERE id_fantasma = %s;",
            (id_fantasma,)
        )
        f = cursor.fetchone()
        novo_xp_f = f['exp_atual'] + xp_ganho
        if novo_xp_f >= f['exp_maxima']:
            novo_xp_f = novo_xp_f - f['exp_maxima']
            upou_f = True
        cursor.execute(
            "UPDATE public.fantasma SET exp_atual = %s WHERE id_fantasma = %s;",
            (novo_xp_f, id_fantasma)
        )
        if upou_f:
            cursor.execute(
                "UPDATE public.fantasma SET ataque_fisico = ataque_fisico + 10, ataque_magico = ataque_magico + 10, defesa_fisica = defesa_fisica + 10, defesa_magica = defesa_magica + 10, nivel = nivel + 1, exp_maxima = exp_maxima + 50, vida_maxima = vida_maxima + 15, vida_atual = vida_maxima WHERE id_fantasma = %s;",
                (id_fantasma,)
            )
            msgs.append("\n==================================\n  \033[1;36mO FANTASMA SUBIU DE NÍVEL!\033[0m\n  Novos atributos, vida e XP máxima aumentados!\n  Vida restaurada!\n==================================\n")
    cursor.connection.commit()
    cursor.connection.close()
    return msgs
