from game.src.interface import Interface
from game.src.operadores.Personagem.criar_personagem import criar_personagem
from game.src.operadores.Personagem.visualizar_personagens import visualizar_personagens
from game.src.database import criar_cursor

def mostrar_descricao_especies():
    """Mostra a descrição detalhada de cada espécie."""
    descricoes = {
        "Zoiudo": "Seres enigmáticos que enxergam além do mundo físico. Dominam os espíritos dos mortos e são mestres da necromancia.",
        "Draconico": "Herdeiros do fogo ancestral. Podem se transformar em dragões e varrer seus inimigos com chamas.",
        "Espiritualista": "Manipuladores da realidade, controlam a essência mágica de Albion. Usam feitiços criativos e poderosos.",
        "Titan": "Colossos de guerra com múltiplos braços. Empunham diversas armas ao mesmo tempo e esmagam tudo em seu caminho."
    }
    
    print(Interface.criar_titulo("Espécies Disponíveis"))
    for especie, descricao in descricoes.items():
        print(f"{Interface.CORES['destaque']}{especie}:")
        print(f"{Interface.CORES['info']}{descricao}\n")

def menu_personagens(id_usuario, username):
    opcoes = ["Criar Personagem", "Visualizar Personagens", "Voltar"]
    
    while True:
        Interface.limpar_tela()
        print(Interface.criar_titulo(f"Menu de Personagens - {username}"))
        
        # Mostra o menu de opções
        print(Interface.criar_menu("Opções", opcoes))
        
        try:
            opcao = int(input()) - 1
            if opcao not in range(len(opcoes)):
                Interface.mostrar_erro("Opção inválida!")
                continue
        except ValueError:
            Interface.mostrar_erro("Por favor, digite um número válido!")
            continue

        cursor = criar_cursor()

        if opcao == 0:  # Criar Personagem
            Interface.limpar_tela()
            print(Interface.criar_titulo("Criar Novo Personagem"))
            
            nome_personagem = input(Interface.criar_elemento("Digite o nome do personagem: ", "menu"))
            
            especies = ["Zoiudo", "Draconico", "Espiritualista", "Titan"]
            mostrar_descricao_especies()
            
            print(Interface.criar_menu("Selecione a espécie do seu personagem:", especies))
            
            try:
                idx = int(input()) - 1
                if idx not in range(len(especies)):
                    Interface.mostrar_erro("Espécie inválida!")
                    continue
            except ValueError:
                Interface.mostrar_erro("Por favor, digite um número válido!")
                continue
                
            especie_personagem = especies[idx]
            
            try:
                criar_personagem(id_usuario, nome_personagem, especie_personagem, cursor)
                Interface.mostrar_sucesso(f"Personagem {nome_personagem} criado com sucesso!")
                input("Pressione ENTER para continuar...")
            except Exception as e:
                Interface.mostrar_erro(f"Erro ao criar personagem: {str(e)}")
                input("Pressione ENTER para continuar...")
                
        elif opcao == 1:  # Visualizar Personagens
            Interface.limpar_tela()
            rows_personagens = visualizar_personagens(id_usuario, cursor)
            return rows_personagens
            
        elif opcao == 2:  # Voltar
            return "voltar"
