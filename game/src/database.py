import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
def conectar_banco():
    try:
        conn = psycopg2.connect(
            dbname = os.getenv("POSTGRES_BD","postgres"),
            user = os.getenv("POSTGRES_USER","postgres"),
            password = os.getenv("POSTGRES_PASSWORD","postgres"),
            host = os.getenv("DATABASE_HOSTNAME", "localhost"),
            port = os.getenv("DATABASE_PORT", 5432)
        )
        print(f"Conexão feita com sucesso: {conn}")
        conn.autocommit = True
        return conn
    
    except psycopg2.Error as e:
        print(f"Erro ao conectar ao banco de dados de albion: {e}")
        return None
    
def criar_cursor():
    conn = conectar_banco()

    if conn:
        try:
            cursor = conn.cursor()
            print("Cursor criado com sucesso!")
            return cursor
        
        except Exception as e:
            print(f"Erro ao criar cursor {e}" )
        
        finally:
            cursor.close()
            conn.close()
    
    else:
        print("Erro ao obter conexão")


criar_cursor()