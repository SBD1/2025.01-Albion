from database import criar_cursor
import math

def calcular_dano_fisico(ataque: int, defesa: int, fator: int = 100) -> int:
    """
    Fórmula de dano: ataque * fator / (defesa + fator)
    Mitigação percentual inspirada em Elder Scrolls.
    Garante retorno decrescente sem zerar o dano (mínimo 1).
    """
    if defesa < 0:
        defesa = 0
    proporcao = ataque * fator / (defesa + fator)
    return max(1, math.floor(proporcao))

def logica_atacar(id_personagem, stamina_atual_personagem, ataque_fisico_personagem, defesa_fisica_monstro, id_instancia, vida_atual_monstro):  
    nova_stamina = max(0, stamina_atual_personagem - 10)
    cursor = criar_cursor()
    cursor.execute(
        "UPDATE public.personagem SET stamina_atual = %s WHERE id_personagem = %s;",
        (nova_stamina, id_personagem)
    )
    # Cálculo de dano baseado em ataque e defesa
    dano_personagem = calcular_dano_fisico(ataque_fisico_personagem, defesa_fisica_monstro)
    nova_vida_monstro = max(0, vida_atual_monstro - dano_personagem)
    cursor.execute(
        "UPDATE public.instancia_npc_generico SET vida_atual = %s WHERE id_instancia = %s;",
        (nova_vida_monstro, id_instancia)
    )

    return nova_stamina, nova_vida_monstro