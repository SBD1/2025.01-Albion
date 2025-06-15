from game.src.interface import Interface
from game.src.database import criar_cursor
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
        Interface.mostrar_erro("Sala atual não encontrada.")
        return

    id_sala_atual = sala_atual['id_sala']
    nome_sala_atual = sala_atual['nome']
    conexoes = {
        "Norte": sala_atual['conexao_norte'],
        "Sul": sala_atual['conexao_sul'],
        "Leste": sala_atual['conexao_leste'],
        "Oeste": sala_atual['conexao_oeste']
    }

    # Busca informações detalhadas da sala atual
    cursor.execute(f"""
        SELECT descricao, tipo
        FROM public.sala
        WHERE id_sala = {id_sala_atual};
    """)
    info_sala = cursor.fetchone()

    opcoes_movimento = []
    for direcao, id_sala_conectada in conexoes.items():
        if id_sala_conectada is not None:
            cursor.execute(f"""
                SELECT nome, tipo, descricao 
                FROM public.sala 
                WHERE id_sala = {id_sala_conectada};
            """)
            sala_conectada = cursor.fetchone()
            if sala_conectada:
                opcoes_movimento.append({
                    'direcao': direcao,
                    'nome': sala_conectada['nome'],
                    'tipo': sala_conectada['tipo'],
                    'descricao': sala_conectada['descricao']
                })

    opcoes_movimento.append({'direcao': 'Voltar', 'nome': 'Voltar ao menu anterior'})

    while True:
        Interface.limpar_tela()
        
        # Mostra a arte ASCII da sala
        print(Interface.CORES['titulo'] + salas[nome_sala_atual])
        
        # Mostra informações da sala atual
        print(Interface.criar_titulo(f"Sala: {nome_sala_atual}"))
        print(f"{Interface.CORES['info']}Tipo: {info_sala['tipo']}")
        print(f"{Interface.CORES['info']}Descrição: {info_sala['descricao']}")
        
        # Mostra as opções de movimento
        print(Interface.criar_titulo("Saídas Disponíveis"))
        for i, opcao in enumerate(opcoes_movimento[:-1], 1):
            print(f"{Interface.CORES['menu']}{i}. {opcao['direcao']} → {opcao['nome']}")
            print(f"{Interface.CORES['info']}   Tipo: {opcao['tipo']}")
            print(f"{Interface.CORES['info']}   {opcao['descricao']}\n")
        
        print(f"{Interface.CORES['menu']}{len(opcoes_movimento)}. {opcoes_movimento[-1]['nome']}")
        print(f"\n{Interface.CORES['normal']}Escolha uma opção: ")
        
        try:
            opcao = int(input()) - 1
            if opcao not in range(len(opcoes_movimento)):
                Interface.mostrar_erro("Opção inválida!")
                continue
        except ValueError:
            Interface.mostrar_erro("Por favor, digite um número válido!")
            continue

        if opcao == len(opcoes_movimento) - 1:  # Voltar
            return "voltar"

        direcao_selecionada = opcoes_movimento[opcao]['direcao']
        nova_sala_id = conexoes[direcao_selecionada]

        cursor.execute(f"""
            UPDATE public.personagem
            SET id_sala = {nova_sala_id}
            WHERE id_personagem = {id_personagem};
        """)
        cursor.connection.commit()
        
        Interface.mostrar_sucesso(f"Você se moveu para {opcoes_movimento[opcao]['nome']} ({direcao_selecionada}).")
        input("Pressione ENTER para continuar...")