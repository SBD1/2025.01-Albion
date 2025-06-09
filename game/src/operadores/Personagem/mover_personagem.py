from simple_term_menu import TerminalMenu
from game.src.database import criar_cursor
from game.src.limpar_tela import limpar_tela
from game.src.ascii_art import salas

def mover_personagem(id_personagem):
    cursor = criar_cursor()
    cursor.execute(f"""
        SELECT s.id_sala, s.nome, s.conexao_norte, s.conexao_sul, s.conexao_leste, s.conexao_oeste
        FROM public.personagem p
        JOIN public.sala s ON p.id_sala = s.id_sala
        WHERE p.id_personagem = {id_personagem};
    """)
    sala_atual = cursor.fetchone()

    if not sala_atual:
        print("❌ ERRO: Sala atual não encontrada.")
        return

    id_sala_atual = sala_atual['id_sala']
    nome_sala_atual = sala_atual['nome']
    conexoes = {
        "Norte": sala_atual['conexao_norte'],
        "Sul": sala_atual['conexao_sul'],
        "Leste": sala_atual['conexao_leste'],
        "Oeste": sala_atual['conexao_oeste']
    }

    opcoes_movimento = []
    for direcao, id_sala_conectada in conexoes.items():
        if id_sala_conectada is not None:
            cursor.execute(f"SELECT nome FROM public.sala WHERE id_sala = {id_sala_conectada};")
            sala_conectada = cursor.fetchone()
            if sala_conectada:
                opcoes_movimento.append(f"{direcao} -> {sala_conectada['nome']}")

    opcoes_movimento.append("Voltar")
    
    print(salas[nome_sala_atual])
    menu = TerminalMenu(
        opcoes_movimento,
        title=f"Você está localizado na: {nome_sala_atual}. Escolha para onde deseja ir:\n",
        menu_cursor_style=("fg_green", "bold"),
        menu_highlight_style=("fg_green", "bold"),
        clear_screen=False
    )
    idx = menu.show()

    if idx == -1 or opcoes_movimento[idx] == "Voltar":
        print("Movimentação cancelada.")
        return "voltar"

    direcao_selecionada = opcoes_movimento[idx].split(" -> ")[0]
    nova_sala_id = conexoes[direcao_selecionada]

    cursor.execute(f"""
        UPDATE public.personagem
        SET id_sala = {nova_sala_id}
        WHERE id_personagem = {id_personagem};
    """)
    cursor.connection.commit()
    
    print(f"✅ Você se moveu para a sala  {opcoes_movimento[idx].split(' -> ')[1]} ({direcao_selecionada}).")
    limpar_tela()