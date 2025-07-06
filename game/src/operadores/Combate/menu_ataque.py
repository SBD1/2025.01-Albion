from game.src.database import criar_cursor
import time
from game.src.limpar_tela import limpar_tela
def logica_atacar(id_personagem, stamina_atual_personagem, ataque_fisico_personagem, defesa_fisica_monstro, id_instancia, vida_atual_monstro):
    nova_stamina = max(0, stamina_atual_personagem - 10)
    cursor = criar_cursor()
    cursor.execute(
        "UPDATE public.personagem SET stamina_atual = %s WHERE id_personagem = %s;",
        (nova_stamina, id_personagem)
    )
    # Calcula dano e atualiza vida do monstro
    dano_personagem = max(0, ataque_fisico_personagem - defesa_fisica_monstro)
    nova_vida_monstro = max(0, vida_atual_monstro - dano_personagem)
    cursor.execute(
        "UPDATE public.instancia_npc_generico SET vida_atual = %s WHERE id_instancia = %s;",
        (nova_vida_monstro, id_instancia)
    )

    limpar_tela()
    print(f"Você causou {dano_personagem} de dano ao monstro.")
    time.sleep(1.5)
    limpar_tela()
    print("=== Turno do Monstro Atacar ===")
    time.sleep(1.5)
    return nova_stamina, nova_vida_monstro