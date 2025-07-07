from game.src.database import criar_cursor
from simple_term_menu import TerminalMenu
from game.src.limpar_tela import limpar_tela
from game.src.operadores.Combate.menu_ataque import calcular_dano_fisico
from game.src.operadores.Combate.menu_magia import calcular_dano_magico
import time

def iniciar_combate_fantasma(
    id_personagem: int,
    fantasma_stats: dict,
    monstro_stats: dict,
    id_instancia: int
) -> tuple[str, int, int]:
    """
    Loop de combate entre fantasma e monstro. Recebe dicts de stats. Retorna (status, vida_fantasma, vida_monstro).
    status: 'cancel', 'fantasma_morreu', 'monstro_morto'
    """
    # Busca informações completas do fantasma (nome, nivel, exp)
    cursor = criar_cursor()
    cursor.execute(
        """
        SELECT F.nome, F.nivel, F.exp_atual, F.exp_maxima
        FROM public.ZOIUDO Z JOIN public.FANTASMA F ON Z.id_fantasma = F.id_fantasma
        WHERE Z.id_personagem = %s;
        """,
        (id_personagem,)
    )
    info_fantasma = cursor.fetchone() or {}
    nome_fantasma = info_fantasma.get('nome', 'Fantasma')
    nivel_fantasma = info_fantasma.get('nivel', '?')
    exp_atual_fantasma = info_fantasma.get('exp_atual', '?')
    exp_maxima_fantasma = info_fantasma.get('exp_maxima', '?')
    vida_maxima_fantasma = fantasma_stats.get('vida_maxima', 1)
    ataque_fisico_fantasma = fantasma_stats.get('ataque_fisico', 0)
    ataque_magico_fantasma = fantasma_stats.get('ataque_magico', 0)
    defesa_fisica_fantasma = fantasma_stats.get('defesa_fisica', 0)
    defesa_magica_fantasma = fantasma_stats.get('defesa_magica', 0)

    vida_maxima_monstro = monstro_stats.get('vida_maxima', 1)
    ataque_fisico_monstro = monstro_stats.get('ataque_fisico', 0)
    ataque_magico_monstro = monstro_stats.get('ataque_magico', 0)
    defesa_fisica_monstro = monstro_stats.get('defesa_fisica', 0)
    defesa_magica_monstro = monstro_stats.get('defesa_magica', 0)
    especie_monstro = monstro_stats.get('especie', 'Monstro')

    vida_atual_fantasma = fantasma_stats.get('vida_atual', vida_maxima_fantasma)
    vida_atual_monstro = monstro_stats.get('vida_atual', vida_maxima_monstro)
    while vida_atual_fantasma > 0 and vida_atual_monstro > 0:
        limpar_tela()
        print("=== Status do Monstro ===")
        print(f"Espécie: {especie_monstro} | Vida: {vida_atual_monstro}/{vida_maxima_monstro}")
        print()
        print("=== Status do Fantasma ===")
        print(f"Nível: {nivel_fantasma} | EXP: {exp_atual_fantasma}/{exp_maxima_fantasma}")
        print(f"Vida: {vida_atual_fantasma}/{vida_maxima_fantasma}")
        print()
        op = ["Atacar", "Cancelar invocação"]
        menu = TerminalMenu(op)
        escolha = menu.show()
        if op[escolha] == "Cancelar invocação":
            status = 'cancel'
            break
        # Fantasma ataca (dano físico + mágico)
        dano_fis = calcular_dano_fisico(ataque_fisico_fantasma, defesa_fisica_monstro)
        dano_mag = calcular_dano_magico(ataque_magico_fantasma, defesa_magica_monstro)
        dano_total = dano_fis + dano_mag
        vida_atual_monstro = max(0, vida_atual_monstro - dano_total)
        cursor = criar_cursor()
        cursor.execute(
            "UPDATE public.instancia_npc_generico SET vida_atual = %s WHERE id_instancia = %s;",
            (vida_atual_monstro, id_instancia)
        )
        limpar_tela()
        print(f"👻 Fantasma causou {dano_fis} 🗡️ físico e {dano_mag} ✨ mágico ao monstro. Total: {dano_total} 💥")
        time.sleep(3)
        if vida_atual_monstro <= 0:
            status = 'monstro_morto_fantasma'
            break
        # Monstro ataca fantasma
        dmg_fis = calcular_dano_fisico(ataque_fisico_monstro, defesa_fisica_fantasma)
        dmg_mag = calcular_dano_magico(ataque_magico_monstro, defesa_magica_fantasma)
        dano_mon = dmg_fis + dmg_mag
        vida_atual_fantasma = max(0, vida_atual_fantasma - dano_mon)
        cursor.execute(
            "UPDATE public.fantasma SET vida_atual = %s WHERE id_fantasma = (SELECT id_fantasma FROM public.zoiudo WHERE id_personagem = %s);",
            (vida_atual_fantasma, id_personagem)
        )
        limpar_tela()
        print(f"👾 Monstro causou {dano_mon} de dano ao fantasma. ({dmg_fis} 🗡️ físico, {dmg_mag} ✨ mágico)")
        time.sleep(3)
        if vida_atual_fantasma <= 0:
            status = 'fantasma_morreu'
            break
    return status, vida_atual_fantasma, vida_atual_monstro

def usar_fantasma(
    id_personagem: int,
    id_instancia: int,
    monstro_stats: dict
) -> tuple[str, int | None, int | None]:
    """
    Executa loop completo de combate do fantasma vs monstro.
    Retorna (status, nova_vida_fantasma, nova_vida_monstro).
    """
    cursor = criar_cursor()
    cursor.execute(
        "SELECT F.vida_atual, F.vida_maxima, F.ataque_fisico, F.ataque_magico, F.defesa_fisica, F.defesa_magica "
        "FROM public.ZOIUDO Z JOIN public.FANTASMA F ON Z.id_fantasma = F.id_fantasma "
        "WHERE Z.id_personagem = %s;",
        (id_personagem,)
    )
    fant = cursor.fetchone()
    if not fant:
        cursor.connection.close()
        print("Seu fantasma não está disponível para lutar.")
        time.sleep(3)
        return 'cancel', None, None
    if fant['vida_atual'] <= 0:
        # Fantasma morto: oferecer opção de reviver
        cursor.execute(
            "SELECT stamina_atual, stamina_maxima FROM public.personagem WHERE id_personagem = %s;",
            (id_personagem,)
        )
        p = cursor.fetchone()
        print("Seu fantasma está morto!")
        print(f"Stamina atual: {p['stamina_atual']} / {p['stamina_maxima']}")
        custo_reviver = p['stamina_maxima'] // 2
        if p['stamina_atual'] < custo_reviver:
            print(f"Stamina insuficiente para reviver o fantasma! (Necessário: pelo menos metade da stamina máxima: {custo_reviver})")
            time.sleep(2)
            cursor.connection.close()
            return 'cancel', None, None
        print(f"Deseja gastar metade da stamina máxima ({custo_reviver}) para reviver o fantasma? (isso irá restaurar o fantasma para vida máxima)")
        menu = TerminalMenu(["Reviver fantasma", "Cancelar"])
        escolha = menu.show()
        if escolha == 0:
            nova_stamina = max(0, p['stamina_atual'] - custo_reviver)
            cursor.execute(
                "UPDATE public.personagem SET stamina_atual = %s WHERE id_personagem = %s;",
                (nova_stamina, id_personagem)
            )
            cursor.execute(
                "UPDATE public.fantasma SET vida_atual = vida_maxima WHERE id_fantasma = (SELECT id_fantasma FROM public.zoiudo WHERE id_personagem = %s);",
                (id_personagem,)
            )
            cursor.connection.commit()
            print("Fantasma revivido!")
            time.sleep(1.5)
            # Recarrega stats do fantasma
            cursor.execute(
                "SELECT F.vida_atual, F.vida_maxima, F.ataque_fisico, F.ataque_magico, F.defesa_fisica, F.defesa_magica "
                "FROM public.ZOIUDO Z JOIN public.FANTASMA F ON Z.id_fantasma = F.id_fantasma "
                "WHERE Z.id_personagem = %s;",
                (id_personagem,)
            )
            fant = cursor.fetchone()
        else:
            cursor.connection.close()
            return 'cancel', None, None
    cursor.connection.close()
    status, vida_f, vida_m = iniciar_combate_fantasma(
        id_personagem,
        fant,
        monstro_stats,
        id_instancia
    )
    return status, vida_f, vida_m
