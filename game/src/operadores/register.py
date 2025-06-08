import psycopg2
def register_user(username, password, cursor):
    if cursor:
        cursor.execute(f"SELECT * FROM USUARIO WHERE username = '{username}'")
        if cursor.fetchone():
            print(f"❌ ERRO: Usuário {username} já existe.")
            return False
        cursor.execute(f"SELECT f_registra_usuario('{username}', '{password}');")
        
        result = cursor.fetchone()
        if result is None:
            print("❌ ERRO: Não foi possível registrar usuário.")
            return False
        print(f"✅ Usuário {username} registrado com sucesso.")
