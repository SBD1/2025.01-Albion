from game.src.database import criar_cursor
from simple_term_menu import TerminalMenu
from game.src.limpar_tela import limpar_tela
from game.src.operadores.Combate.menu_ataque import logica_atacar, calcular_dano_fisico
from game.src.operadores.Combate.menu_magia import menu_magia
from game.src.operadores.drops.menu_drop import checar_drops

import time

def checar_personagem(id_personagem):
    cursor = criar_cursor()
    if not cursor:
        print("Erro ao criar o cursor")
    
    try:
        query = "SELECT * FROM PERSONAGEM WHERE id_personagem = %s"
        cursor.execute(query, (id_personagem,))
        personagem = cursor.fetchone()
        if not personagem:
            print("Personagem não encontrado")
            return

    except Exception as e:
        print("Erro ao capturar informações do personagem:", e)
        return
    
    return personagem

def checar_especie(id_personagem):

    cursor = criar_cursor()
    # zoiúdo
    cursor.execute("SELECT 1 FROM ZOIUDO WHERE id_personagem=%s;", (id_personagem,))
    especie = cursor.fetchone()
    if especie:
        id_especie = 1

    # espiritualista
    cursor.execute("SELECT 1 FROM ESPIRITUALISTA WHERE id_personagem=%s;", (id_personagem,))
    especie = cursor.fetchone()
    if especie:
        id_especie = 2

    # dracônico
    cursor.execute("SELECT 1 FROM DRACONICO WHERE id_personagem=%s;", (id_personagem,))
    especie = cursor.fetchone()
    if especie:
        id_especie = 3

    # titan
    cursor.execute("SELECT 1 FROM TITAN WHERE id_personagem=%s;", (id_personagem,))
    especie = cursor.fetchone()
    if especie:
        id_especie = 4
    
    cursor.connection.close()
    return id_especie, especie

def checar_instancia(id_instancia):
    cursor = criar_cursor()
    if not cursor:
        print("Erro ao criar o cursor")
        return

    try:
        cursor.execute(
            "SELECT * FROM INSTANCIA_NPC_GENERICO WHERE id_instancia = %s;",
            (id_instancia,)
        )
        npc_instancia = cursor.fetchone()
        if not npc_instancia:
            print("Instancia não encontrada")
            return
        return npc_instancia
    except Exception as e:
        print("Erro ao capturar INSTANCIA_NPC_GENERICO:", e)
        return

def iniciar_combate(id_personagem, id_sala):

    # Capturando informações da tabela NPC
    cursor = criar_cursor()
    if not cursor:
        print("Erro ao criar o cursor")
        return
    
    try:
        cursor.execute("SELECT * FROM NPC WHERE id_sala = %s", (id_sala,))
        npc = cursor.fetchone()
        if not npc:
            print("NPC não encontrado")
            return
    except Exception as e:
        print("Erro ao capturar NPC:", e)
        return
    
    # Capturando informações da tabela NPC_GENERICO
    try:
        cursor.execute(
            "SELECT * FROM NPC_GENERICO WHERE id_npc = %s", 
            (npc['id_npc'],)
        )
        npc_gen = cursor.fetchone()
        if not npc_gen:
            print("NPC_GENERICO não encontrado")
            return
    except Exception as e:
        print("Erro ao capturar NPC_GENERICO:", e)
        return
    
    # Criando instância de NPC_GENERICO
    try:
        cursor.execute(
            "SELECT f_cria_instancia_npc_generico(%s) AS id_instancia;",
            (npc_gen['id_npc'],)
        )
        result = cursor.fetchone()
        id_instancia = result.get('id_instancia')
        print(f"Instância criada: {id_instancia}")
    except Exception as e:
        print("Erro ao criar instância de NPC_GENERICO:", e)
        return
    cursor.connection.close()
    
    # Inicializa variáveis de combate
    monstro = checar_instancia(id_instancia)
    if not monstro:
        return
    vida_maxima_monstro = npc_gen['vida_maxima']
    vida_atual_monstro = monstro['vida_atual']
    ataque_fisico_monstro = npc_gen['ataque_fisico']
    ataque_magico_monstro = npc_gen['ataque_magico']
    defesa_fisica_monstro = npc_gen['defesa_fisica']
    defesa_magica_monstro = npc_gen['defesa_magica']

    personagem = checar_personagem(id_personagem)
    if not personagem:
        return
    vida_maxima_personagem = personagem['vida_maxima']
    vida_atual_personagem = personagem['vida_atual']
    ataque_fisico_personagem = personagem['ataque_fisico']
    defesa_fisica_personagem = personagem['defesa_fisica']
    defesa_magica_personagem = personagem['defesa_magica']
    stamina_maxima_personagem = personagem['stamina_maxima']
    stamina_atual_personagem = personagem['stamina_atual']
    id_especie, _ = checar_especie(id_personagem)

    # Loop de combate com turnos alternados
    turno = 'personagem'
    while vida_atual_monstro > 0 and vida_atual_personagem > 0:
        limpar_tela()
        print("=== Status do Monstro ===")
        print(f"Espécie: {npc['especie']} | Vida: {vida_atual_monstro}/{vida_maxima_monstro}")
        print()
        print("=== Status do Personagem ===")
        print(f"Nome: {personagem['nome']} | Nível: {personagem['nivel']} | EXP: {personagem['exp_atual']}/{personagem['exp_maxima']}")
        print(f"Vida: {vida_atual_personagem}/{vida_maxima_personagem} | Stamina: {stamina_atual_personagem}/{stamina_maxima_personagem}")
        print()

        # Turno Personagem
        if turno == 'personagem':
            # Menu Combate
            opcoes = ["Atacar"]
            if id_especie == 1:
                opcoes.append("Atacar com fantasma")
            elif id_especie == 2:
                opcoes.append("Usar Magia")
            elif id_especie == 3:
                opcoes.append("Usar transformação")
            
            opcoes.extend(["Abrir inventário", "Fugir"])
            menu = TerminalMenu(opcoes)
            escolha = menu.show()
            acao = opcoes[escolha]

            if acao == "Fugir":
                print("=== Você fugiu do combate! ===")
                break
            
            # Lógica de ataque normal
            if acao == "Atacar":
                stamina_atual_personagem, vida_atual_monstro = logica_atacar(
                    id_personagem,
                    stamina_atual_personagem,
                    ataque_fisico_personagem,
                    defesa_fisica_monstro,
                    id_instancia,
                    vida_atual_monstro
                )
                turno = 'monstro'

            elif acao == "Usar Magia":
                usar_magia()
            else:
                # Outras ações mantêm turno do jogador, adiconar depois
                continue

        # Ataque do monstro com cálculo percentual de dano
        dmg_fisico = calcular_dano_fisico(ataque_fisico_monstro, defesa_fisica_personagem)
        dmg_magico = calcular_dano_fisico(ataque_magico_monstro, defesa_magica_personagem)
        dano_monstro = dmg_fisico + dmg_magico
        vida_atual_personagem = max(0, vida_atual_personagem - dano_monstro)
        criar_cursor().execute(
            "UPDATE PERSONAGEM SET vida_atual = %s WHERE id_personagem = %s;",
            (vida_atual_personagem, id_personagem)
        )

        limpar_tela()
        print(f"O monstro causou {dano_monstro} de dano (Fisico:{dmg_fisico} e Magico:{dmg_magico}).")
        time.sleep(1.5)

        limpar_tela()
        print("=== Seu turno de Ação ===")
        time.sleep(1.5)
        turno = 'personagem'
        
        continue

    # Verifica se o monstro foi derrotado
    if vida_atual_monstro <= 0:
        limpar_tela()
        print(f"Você derrotou o monstro! Ganhou {npc_gen['xp']} de xp")
        time.sleep(1.5)
        xp_monstro = npc_gen['xp']
        xp_atual = personagem['exp_atual']
        novo_xp = xp_atual + xp_monstro
        cursor = criar_cursor()
        cursor.execute(
            "UPDATE public.personagem SET exp_atual = %s WHERE id_personagem = %s;",
            (novo_xp, id_personagem)
        )
        cursor.connection.commit()
        print(f"Você ganhou {xp_monstro} pontos de EXP.")
        time.sleep(1.5)

        # Checa drops
        #checar_drops(id_instancia)
        time.sleep(1.5)

    # Verifica se o personagem morreu
    if vida_atual_personagem <= 0:
        limpar_tela()
        print("Você foi derrotado pelo monstro e morreu!")
        time.sleep(1.5)

        # Reduz 10% do XP atual
        xp_atual = personagem['exp_atual']
        perda_xp = int(xp_atual * 0.1)
        novo_xp = max(0, xp_atual - perda_xp)

        # Atualiza EXP, sala e vida
        cursor = criar_cursor()
        cursor.execute(
            "UPDATE public.personagem SET exp_atual = %s WHERE id_personagem = %s;",
            (novo_xp, id_personagem)
        )
        cursor.execute(
            "UPDATE public.personagem SET id_sala = %s WHERE id_personagem = %s;",
            (1, id_personagem)
        )
        cursor.execute(
            "UPDATE public.personagem SET vida_atual = %s WHERE id_personagem = %s;",
            (vida_maxima_personagem, id_personagem)
        )
        cursor.connection.commit()
        print(f"Você perdeu {perda_xp} pontos de EXP.")
        time.sleep(1.5)
        limpar_tela()
        print("Você foi levado para a Praça Central para receber cuidados.")
        time.sleep(1.5)

        menu = TerminalMenu(["OK"], title="Pressione OK para retornar ao mapa.")
        menu.show()
        return "mudar_sala"
    
    return
