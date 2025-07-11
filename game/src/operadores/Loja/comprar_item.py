from simple_term_menu import TerminalMenu
from database import criar_cursor
from limpar_tela import limpar_tela

def comprar_item(id_personagem, id_item):
    cursor = criar_cursor()

    try:
        # Obter informações do item na loja
        cursor.execute("""
            SELECT li.preco, li.quantidade_disponivel, i.nome
            FROM LOJA_ITENS li
            JOIN ITEM i ON li.id_item = i.id_item
            WHERE li.id_item = %s;
        """, (id_item,))
        item = cursor.fetchone()

        if not item:
            print("❌ Item não encontrado na loja.")
            return

        preco = item['preco']
        quantidade_disponivel = item['quantidade_disponivel']
        nome_item = item['nome']

        # Verificar se o item está disponível
        if quantidade_disponivel <= 0:
            print(f"❌ O item '{nome_item}' está esgotado.")
            return

        # Obter o ouro do personagem
        cursor.execute("""
            SELECT qtd_ouro
            FROM PERSONAGEM
            WHERE id_personagem = %s;
        """, (id_personagem,))
        personagem = cursor.fetchone()

        if not personagem:
            print("❌ Personagem não encontrado.")
            return

        qtd_ouro = personagem['qtd_ouro']

        # Verificar se o personagem tem ouro suficiente
        if qtd_ouro < preco:
            print(f"❌ Ouro insuficiente. Você precisa de {preco} ouro, mas tem apenas {qtd_ouro}.")
            return

        # Atualizar o ouro do personagem
        cursor.execute("""
            UPDATE PERSONAGEM
            SET qtd_ouro = qtd_ouro - %s
            WHERE id_personagem = %s;
        """, (preco, id_personagem))

        # Adicionar o item ao inventário
        cursor.execute("""
            SELECT f_insere_item(%s, %s, 1);
        """, (id_personagem, id_item))

        # Atualizar a quantidade disponível na loja
        cursor.execute("""
            UPDATE LOJA_ITENS
            SET quantidade_disponivel = quantidade_disponivel - 1
            WHERE id_item = %s;
        """, (id_item,))

        # Confirmar as alterações no banco de dados
        cursor.connection.commit()

        print(f"✅ Você comprou {nome_item} por {preco} ouro.")
    except Exception as e:
        print(f"❌ Erro ao comprar item: {e}")
        cursor.connection.rollback()
    finally:
        cursor.close()
