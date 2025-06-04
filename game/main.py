import psycopg2
from psycopg2.extras import RealDictCursor
import os

def criar_conta(username, senha, conn, cur):
    cur.execute("SELECT * FROM USUARIO WHERE username = %s AND senha = %s",(username,senha))
    existe_usuario = cur.fetchall()
    if existe_usuario:
        return None
    cur.execute("INSERT INTO USUARIO(username, senha) VALUES (%s, %s) RETURNING id_usuario;",(username,senha))
    userId = cur.fetchone()
    conn.commit()
    return userId

def validar_login(username, senha, cur):
    cur.execute("SELECT * FROM USUARIO WHERE username = %s AND senha = %s",(username,senha))
    user = cur.fetchall()
    if user:
        print(user)
        return user[0]
    return None



def main():
    print("Albion")
if __name__ == "__main__":
    main()