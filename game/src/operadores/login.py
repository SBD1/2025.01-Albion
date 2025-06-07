from src.database import criar_cursor
def verificar_usuario(nome,senha):
    conn,cursor = criar_cursor()

    if conn and cursor:
        try:
            sql = """select id 
            from usuario 
            where username = %s and password = %s"""

            cursor.execute(sql,(nome,senha))
            resultado = cursor.fetchone()
            
            if resultado:
                id = resultado[0]
                print("Resultado encontrado!")

            else:
                print('Usuario não encontrado')
                return None

        except Exception as e:
            print(f"Erro ao verificar usuario: {e}")
            return None

        finally:
            conn.close()
            cursor.close()

    return id

def visu_persos(nome,password):
    id =  verificar_usuario(nome, password)
    
    sql = """select distinct nome, raça, nivel
    from personagem
    where id = %s """