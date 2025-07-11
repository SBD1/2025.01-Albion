def criar_personagem(id_usuario, nome_personagem, especie_personagem, cursor):
    if cursor:
        cursor.execute(f"SELECT f_cria_personagem({id_usuario}, '{nome_personagem}', '{especie_personagem}');")
        id_personagem = cursor.fetchone()['f_cria_personagem']
        
        if id_personagem is None:
            return False
        
        return True