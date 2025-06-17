from game.src.interface import Interface

def visualizar_personagens(id_usuario, cursor):
    cursor.execute(f"""
    SELECT 
        p.id_personagem,
        p.nome, 
        p.nivel, 
        p.qtd_ouro, 
        p.vida,
        p.vida_maxima,
        p.forca,
        p.defesa,
        s.nome AS nome_sala,
        CASE 
            WHEN z.id_personagem IS NOT NULL THEN 'Zoiudo'
            WHEN e.id_personagem IS NOT NULL THEN 'Espiritualista'
            WHEN d.id_personagem IS NOT NULL THEN 'Draconico'
            WHEN t.id_personagem IS NOT NULL THEN 'Titan'
            ELSE 'Desconhecido'
        END AS especie
    FROM public.personagem p
        LEFT JOIN public.zoiudo z ON p.id_personagem = z.id_personagem
        LEFT JOIN public.espiritualista e ON p.id_personagem = e.id_personagem
        LEFT JOIN public.draconico d ON p.id_personagem = d.id_personagem
        LEFT JOIN public.titan t ON p.id_personagem = t.id_personagem
        JOIN public.sala s ON p.id_sala = s.id_sala
    WHERE 
        p.id_usuario = {id_usuario};""")

    rows = cursor.fetchall()
    
    if not rows:
        Interface.mostrar_erro("Nenhum personagem encontrado.")
        input("Pressione ENTER para continuar...")
        return None
    
    Interface.limpar_tela()
    print(Interface.criar_titulo("Seus Personagens"))
    
    for i, personagem in enumerate(rows, 1):
        print(Interface.criar_borda(f"Personagem {i}"))
        print(f"{Interface.CORES['destaque']}Nome: {personagem['nome']}")
        print(f"{Interface.CORES['info']}Espécie: {personagem['especie']}")
        print(f"{Interface.CORES['menu']}Nível: {personagem['nivel']}")
        print(f"{Interface.CORES['sucesso']}Vida: {personagem['vida']}/{personagem['vida_maxima']}")
        print(f"{Interface.CORES['erro']}Força: {personagem['forca']}")
        print(f"{Interface.CORES['info']}Defesa: {personagem['defesa']}")
        print(f"{Interface.CORES['menu']}Ouro: {personagem['qtd_ouro']}")
        print(f"{Interface.CORES['info']}Localização: {personagem['nome_sala']}\n")
    
    print(Interface.criar_menu("Escolha um personagem:", [f"{p['nome']} (Nível {p['nivel']} {p['especie']})" for p in rows]))
    
    try:
        opcao = int(input()) - 1
        if opcao not in range(len(rows)):
            Interface.mostrar_erro("Opção inválida!")
            return None
    except ValueError:
        Interface.mostrar_erro("Por favor, digite um número válido!")
        return None
    
    return rows

    