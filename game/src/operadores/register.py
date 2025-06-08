import psycopg2
from database import criar_cursor

def register_user(username, password):
    conn, cursor = criar_cursor()
    if conn and cursor:
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
