def login(nome,senha,cursor):

    if cursor:
        try:
            sql = """select id_usuario 
            from public.usuario 
            where username = %s and password = %s"""

            cursor.execute(sql,(nome,senha))
            resultado = cursor.fetchone()
            
            if resultado:
                id = resultado["id_usuario"]
                #print("Usuario encontrado!")

            else:
                print('Usuario não encontrado')
                return None

        except Exception as e:
            print(f"Erro ao verificar usuario: {e}")
            return None

    return id
