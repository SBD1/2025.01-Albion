from database import criar_cursor
from simple_term_menu import TerminalMenu
from limpar_tela import limpar_tela
from game.src.operadores.Combate.logica_ataque import logica_atacar, calcular_dano_fisico
from operadores.Combate.menu_magia import menu_magia
from operadores.Combate.menu_transformacao import menu_transformacao_draconico, iniciar_combate_draconico
from operadores.Combate.menu_fantasma import usar_fantasma
from operadores.Combate.xp import aplicar_xp
from operadores.Inventario.menu_inventario_pygame import menu_inventario_pygame
from operadores.Menus.estrutura_menu_pygame import MenuPyGame
# from operadores.drops.menu_drop import checar_drops

import time

def atualizar_stats_personagem(id_personagem):
    """
    Função utilitária para buscar stats atualizados do personagem no banco de dados.
    Retorna um dicionário com os stats atuais incluindo bônus de equipamentos.
    """
    from operadores.Personagem.calcular_atributos import calcular_atributos_totais_personagem
    
    try:
        return calcular_atributos_totais_personagem(id_personagem)
    except Exception as e:
        print(f"Erro ao atualizar stats do personagem: {e}")
        # Fallback para função simples
        cursor = criar_cursor()
        if not cursor:
            return None
        
        try:
            query = "SELECT * FROM PERSONAGEM WHERE id_personagem = %s"
            cursor.execute(query, (id_personagem,))
            personagem = cursor.fetchone()
            cursor.connection.close()
            return personagem
        except Exception as e2:
            print(f"Erro no fallback: {e2}")
            if cursor:
                cursor.connection.close()
            return None

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
    if not cursor:
        return None, None
    try:
        # Verifica cada espécie na ordem de prioridade
        cursor.execute("SELECT 1 FROM ZOIUDO WHERE id_personagem=%s;", (id_personagem,))
        if cursor.fetchone():
            return 1, 'zoiudo'
        cursor.execute("SELECT 1 FROM ESPIRITUALISTA WHERE id_personagem=%s;", (id_personagem,))
        if cursor.fetchone():
            return 2, 'espiritualista'
        cursor.execute("SELECT 1 FROM DRACONICO WHERE id_personagem=%s;", (id_personagem,))
        if cursor.fetchone():
            return 3, 'draconico'
        cursor.execute("SELECT 1 FROM TITAN WHERE id_personagem=%s;", (id_personagem,))
        if cursor.fetchone():
            return 4, 'titan'
        # Nenhuma espécie correspondente
        return None, None
    finally:
        cursor.connection.close()

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
    menu = MenuPyGame()
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
    monstro_stats = {
        'vida_atual': vida_atual_monstro,
        'vida_maxima': vida_maxima_monstro,
        'ataque_fisico': ataque_fisico_monstro,
        'ataque_magico': ataque_magico_monstro,
        'defesa_fisica': defesa_fisica_monstro,
        'defesa_magica': defesa_magica_monstro
    }

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

    # Inicializa MenuPyGame e seleção padrão
    menu = MenuPyGame()
    selected = 0

    # Loop de combate com turnos alternados
    turno = 'personagem'
    while vida_atual_monstro > 0 and vida_atual_personagem > 0:
        # Monta status sem tracking de turnos dracônico
        status_info = {
             'monstro': {
                 'especie': npc['especie'], 'vida_atual': vida_atual_monstro, 'vida_maxima': vida_maxima_monstro
             },
             'personagem': {
                 'nome': personagem['nome'], 'nivel': personagem['nivel'],
                 'exp_atual': personagem['exp_atual'], 'exp_maxima': personagem['exp_maxima'],
                 'vida_atual': vida_atual_personagem, 'vida_maxima': vida_maxima_personagem,
                 'stamina_atual': stamina_atual_personagem, 'stamina_maxima': stamina_maxima_personagem,
                 'ataque_fisico': ataque_fisico_personagem
             }
        }
        # Define opções de ação conforme espécie
        opcoes_combate = ["⚔️ Atacar"]
        if id_especie == 1:
            opcoes_combate.append("👻 Invocar Fantasma")
        elif id_especie == 2:
            opcoes_combate.append("✨ Usar Magia")
        elif id_especie == 3:
            opcoes_combate.append("🔥 Transformação Dracônica")
        elif id_especie == 4:
            opcoes_combate.append("💪 Habilidade Titan")
        opcoes_combate += ["🎒 Inventário", "🏃 Fugir"]
        escolha = menu.set_menu_combate("⚔️ COMBATE ⚔️", status_info, opcoes_combate, selected)
        selected = escolha if escolha >= 0 else selected
        acao = opcoes_combate[escolha] if escolha >= 0 else None
        limpar_tela()

        # Ação do personagem selecionada via Pygame
        if acao == "⚔️ Atacar":
            # Jogador ataca
            dano_previo = vida_atual_monstro
            stamina_atual_personagem, vida_atual_monstro = logica_atacar(
                id_personagem,
                stamina_atual_personagem,
                ataque_fisico_personagem,
                defesa_fisica_monstro,
                id_instancia,
                vida_atual_monstro
            )
            dano_causado = dano_previo - vida_atual_monstro
            menu.feedback("ATAQUE", f"Você causou {dano_causado} de dano!", duration=3000)

            # Se monstro morrer
            if vida_atual_monstro <= 0:
                menu.feedback("VITÓRIA", f"{npc['especie']} derrotado!", duration=4000)
                
                # Adiciona ouro do drop ao personagem
                ouro_drop = npc_gen['drop_ouro']
                cursor_ouro = criar_cursor()
                cursor_ouro.execute(
                    "UPDATE PERSONAGEM SET qtd_ouro = qtd_ouro + %s WHERE id_personagem = %s;",
                    (ouro_drop, id_personagem)
                )
                cursor_ouro.connection.commit()
                cursor_ouro.connection.close()
                menu.feedback("OURO", f"Você ganhou {ouro_drop} moedas de ouro!", duration=3000)
                
                xp_monstro = npc_gen['xp']
                for msg in aplicar_xp(id_personagem, xp_monstro):
                    menu.feedback("XP", msg, duration=3000)
                return "vitoria"
            
            # Turno do monstro
            menu.feedback("TURNO", "É a vez do monstro!", duration=3000)
            dmg_fisico = calcular_dano_fisico(ataque_fisico_monstro, defesa_fisica_personagem)
            dmg_magico = calcular_dano_fisico(ataque_magico_monstro, defesa_magica_personagem)
            dano_monstro = dmg_fisico + dmg_magico
            vida_atual_personagem = max(0, vida_atual_personagem - dano_monstro)
            criar_cursor().execute(
                "UPDATE PERSONAGEM SET vida_atual = %s WHERE id_personagem = %s;",
                (vida_atual_personagem, id_personagem)
            )
            menu.feedback("ATAQUE INIMIGO", f"Você recebeu {dano_monstro} de dano!", duration=3000)
            
            # Se jogador morrer
            if vida_atual_personagem <= 0:
                cursor_f = criar_cursor()
                # Reduz 10% de EXP
                xp_atual = personagem['exp_atual']
                perda_xp = int(xp_atual * 0.1)
                novo_xp = max(0, xp_atual - perda_xp)
                cursor_f.execute("UPDATE public.personagem SET exp_atual = %s WHERE id_personagem = %s;", (novo_xp, id_personagem))
                # Teleporta para sala 1
                cursor_f.execute("UPDATE public.personagem SET id_sala = 1 WHERE id_personagem = %s;", (id_personagem,))
                # Restaura vida e stamina
                cursor_f.execute("UPDATE public.personagem SET vida_atual = %s, stamina_atual = %s WHERE id_personagem = %s;", (vida_maxima_personagem, stamina_maxima_personagem, id_personagem))
                # Restaura mana do espiritualista
                cursor_f.execute("UPDATE public.espiritualista SET mana_atual = mana_total WHERE id_personagem = %s;", (id_personagem,))
                # Restaura vida do fantasma
                id_esp, _ = checar_especie(id_personagem)
                if id_esp == 1:
                    cursor_f.execute(
                        "UPDATE public.fantasma SET vida_atual = vida_maxima WHERE id_fantasma = (SELECT id_fantasma FROM public.zoiudo WHERE id_personagem = %s);", (id_personagem,)
                    )
                cursor_f.connection.commit()
                menu.feedback("DERROTA", f"Você morreu e foi teleportado para a Praça Central! Perdeu {perda_xp} EXP.", duration=4000)
                return "derrota"
        
            menu.feedback("TURNO", "Seu turno!", duration=3000)
            continue

        # Chama menu fantasma
        elif acao == "👻 Invocar Fantasma":
            prev_monstro = vida_atual_monstro
            status_f, vida_f, vida_m_nova = usar_fantasma(
                id_personagem, id_instancia, monstro_stats
            )
            
            # Atualizar stats após usar fantasma (stamina gasta)
            personagem_atualizado = atualizar_stats_personagem(id_personagem)
            if personagem_atualizado:
                stamina_atual_personagem = personagem_atualizado['stamina_atual']
            
            if status_f == 'cancel':
                continue

            if status_f == 'fantasma_morreu':
                menu.feedback("FANTASMA", "Seu fantasma foi derrotado!", duration=2000)
                menu.feedback("TURNO", "É o seu turno!", duration=1000)
                continue

            if status_f == 'monstro_morto_fantasma':
                menu.feedback("VITÓRIA", f"{npc['especie']} derrotado pelo Fantasma!", duration=2000)
                
                # Adiciona ouro do drop ao personagem
                ouro_drop = npc_gen['drop_ouro']
                cursor_ouro = criar_cursor()
                cursor_ouro.execute(
                    "UPDATE PERSONAGEM SET qtd_ouro = qtd_ouro + %s WHERE id_personagem = %s;",
                    (ouro_drop, id_personagem)
                )
                cursor_ouro.connection.commit()
                cursor_ouro.connection.close()
                menu.feedback("OURO", f"Você ganhou {ouro_drop} moedas de ouro!", duration=2000)
                
                xp_valor = npc_gen['xp']
                for msg in aplicar_xp(id_personagem, xp_valor):
                    menu.feedback("XP", msg, duration=2000)
                return "vitoria"
            
            # Fantasma causou dano parcial
            if vida_m_nova is not None:
                vida_atual_monstro = vida_m_nova
                dano_f = prev_monstro - vida_atual_monstro
                menu.feedback("ATAQUE FANTASMA", f"Fantasma causou {dano_f} de dano!", duration=2000)

                menu.feedback("TURNO", "É a vez do monstro!", duration=1000)
                fis = calcular_dano_fisico(ataque_fisico_monstro, defesa_fisica_personagem)
                mag = calcular_dano_fisico(ataque_magico_monstro, defesa_magica_personagem)
                dmg_tot = fis + mag
                vida_atual_personagem = max(0, vida_atual_personagem - dmg_tot)
                criar_cursor().execute(
                    "UPDATE PERSONAGEM SET vida_atual = %s WHERE id_personagem = %s;",
                    (vida_atual_personagem, id_personagem)
                )
                menu.feedback("ATAQUE INIMIGO", f"Monstro causou {dmg_tot} de dano!", duration=1500)
                if vida_atual_personagem <= 0:
                    # Jogador morreu
                    menu.feedback("DERROTA", "Você morreu!", duration=2000)
                    return "derrota"
                # Retorno ao jogador
                menu.feedback("TURNO", "Seu turno!", duration=1000)
                continue

        elif acao == "✨ Usar Magia":
            # Executa magia e mostra feedback de dano mágico
            vida_antiga = vida_atual_monstro
            resultado = menu_magia(
                id_personagem,
                id_instancia,
                monstro_stats
            )
            
            # Atualizar stats após usar magia (mana gasta)
            personagem_atualizado = atualizar_stats_personagem(id_personagem)
            if personagem_atualizado:
                stamina_atual_personagem = personagem_atualizado['stamina_atual']
            
            if resultado and resultado[0] is not None and resultado[1] is not None:
                vida_atual_monstro = resultado[1]
                dano_magico_turno = vida_antiga - vida_atual_monstro
                menu.feedback("MAGIA", f"Você causou {dano_magico_turno} de dano mágico!", duration=2000)
                
                # Verifica se o monstro morreu com a magia
                if vida_atual_monstro <= 0:
                    menu.feedback("VITÓRIA", f"{npc['especie']} derrotado pela magia!", duration=4000)
                    
                    # Adiciona ouro do drop ao personagem
                    ouro_drop = npc_gen['drop_ouro']
                    cursor_ouro = criar_cursor()
                    cursor_ouro.execute(
                        "UPDATE PERSONAGEM SET qtd_ouro = qtd_ouro + %s WHERE id_personagem = %s;",
                        (ouro_drop, id_personagem)
                    )
                    cursor_ouro.connection.commit()
                    cursor_ouro.connection.close()
                    menu.feedback("OURO", f"Você ganhou {ouro_drop} moedas de ouro!", duration=3000)
                    
                    xp_monstro = npc_gen['xp']
                    for msg in aplicar_xp(id_personagem, xp_monstro):
                        menu.feedback("XP", msg, duration=3000)
                    return "vitoria"
                
                turno = 'monstro'
            else:
                continue
            
        elif acao == "🔥 Transformação Dracônica":
            # Transição para submenu dracônico
            trans = menu_transformacao_draconico(id_personagem)
            if not trans:
                continue
            # Inicia combate específico de dracônico
            status = iniciar_combate_draconico(id_personagem, id_instancia, monstro_stats)
            
            # Atualizar stats do personagem após retornar do submenu dracônico
            personagem_atualizado = atualizar_stats_personagem(id_personagem)
            if personagem_atualizado:
                vida_atual_personagem = personagem_atualizado['vida_atual']
                ataque_fisico_personagem = personagem_atualizado['ataque_fisico']
                stamina_atual_personagem = personagem_atualizado['stamina_atual']
                defesa_fisica_personagem = personagem_atualizado['defesa_fisica']
                defesa_magica_personagem = personagem_atualizado['defesa_magica']
            
            # Bônus aplicados e revertidos pelo menu_transformacao_draconico
            # Fecha submenu e retorna ao combate principal
            if status == 'vitoria':
                return 'vitoria'
            elif status == 'derrota':
                return 'derrota'
            continue
        elif acao == "🎒 Inventário":
            inv_res = menu_inventario_pygame(id_personagem)
            if inv_res in (-1, 'voltar'):
                # Atualizar stats após usar inventário (caso tenha consumido poções/itens)
                personagem_atualizado = atualizar_stats_personagem(id_personagem)
                if personagem_atualizado:
                    vida_atual_personagem = personagem_atualizado['vida_atual']
                    stamina_atual_personagem = personagem_atualizado['stamina_atual']
                    ataque_fisico_personagem = personagem_atualizado['ataque_fisico']
                    defesa_fisica_personagem = personagem_atualizado['defesa_fisica']
                    defesa_magica_personagem = personagem_atualizado['defesa_magica']
                time.sleep(1.5); continue
        elif acao == "🏃 Fugir":
            # Fuga do combate
            menu.feedback("FUGA", "Você fugiu com sucesso!", duration=3000)
            return "fugir"

        # O turno do monstro agora está integrado diretamente após o ataque do jogador

        limpar_tela()
        time.sleep(1)
        turno = 'personagem'
        
        continue
    
    # Verifica se o personagem morreu
    if vida_atual_personagem <= 0:
        limpar_tela()
        print("Você foi derrotado pelo monstro e morreu!")
        time.sleep(3)

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
        cursor.execute(
            "UPDATE public.personagem SET stamina_atual = %s WHERE id_personagem = %s;",
            (stamina_maxima_personagem, id_personagem)
        )
        # Restaura mana do espiritualista ao máximo
        cursor.execute(
            "UPDATE public.espiritualista SET mana_atual = mana_total WHERE id_personagem = %s;",
            (id_personagem,)
        )
        # Restaura vida do fantasma ao máximo se for Zoiudo
        id_especie, _ = checar_especie(id_personagem)
        if id_especie == 1:
            cursor.execute(
                "UPDATE public.fantasma SET vida_atual = vida_maxima WHERE id_fantasma = (SELECT id_fantasma FROM public.zoiudo WHERE id_personagem = %s);",
                (id_personagem,)
            )
        cursor.connection.commit()
        print(f"Você perdeu {perda_xp} pontos de EXP.")
        time.sleep(3)
        limpar_tela()
        print("Você foi levado para a Praça Central para receber cuidados.")
        time.sleep(3)

        menu = TerminalMenu(["OK"], title="Pressione OK para retornar ao mapa.")
        menu.show()
        return "mudar_sala"
    
    return
