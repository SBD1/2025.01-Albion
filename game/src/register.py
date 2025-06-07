import psycopg2
from database import criar_cursor

def register_user(username, password):
    conn, cursor = criar_cursor()
    if conn and cursor:
        try:
            cursor.execute(f"SELECT f_registra_usuario('{username}', '{password}');")
            result = cursor.fetchone()
            if result is None or not result[0]:
                print("ERRO APÓS QUERY")
                return False
            print(f"Usuário {username} registrado com sucesso.")
            
        except Exception as e:
            print(f"Erro ao criar usuário: {e}")
            return False


username = 'teste'
password = '123'
register_user(username, password)