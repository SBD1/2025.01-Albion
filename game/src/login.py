from database import criar_cursor

def verificar_usuario(nome,senha):
    conn,cursor = criar_cursor()

    if conn and cursor:
        try:
            sql = """select id_usuario 
            from public.usuario 
            where username = %s and password = %s"""

            cursor.execute(sql,(nome,senha))
            resultado = cursor.fetchone()
            
            if resultado:
                id = resultado["id_usuario"]
                print("Resultado encontrado!")
                visualizar_personagens(id,cursor)

            else:
                print('Usuario não encontrado')
                return None

        except Exception as e:
            print(f"Erro ao verificar usuario: {e}")
            return None

        finally:
            conn.close()
            cursor.close()

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


verificar_usuario("Alo","123")