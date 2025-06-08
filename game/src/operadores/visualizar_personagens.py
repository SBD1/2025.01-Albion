def visualizar_personagens(id,cursor):
    try:
        sql = """select distinct nome, raça, nivel
        from personagem
        where id = %s """

        cursor.execute(sql,(id))
        resultado = cursor.fetchall()

        if resultado:
            print("Personagem(s) encontrado(s): ")
            for personagem in resultado:
                print(personagem)
            
        else:
            print("Nenhum personagem encontrado.")

    except Exception as e:
        print(f"Erro ao encontrar personagens: {e}")

    return resultado