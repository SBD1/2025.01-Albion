def criar_personagem(id_usuario, nome_personagem, especie_personagem, cursor):
    if cursor:
        try:
            cursor.execute(f"SELECT f_cria_personagem({id_usuario}, '{nome_personagem}', '{especie_personagem}');")
            id_personagem = cursor.fetchone()['f_cria_personagem']
            
            if id_personagem is None:
                print("❌ ERRO: Não foi possível criar personagem.\n")
                return False
            
            print(f"✅ Personagem criado com sucesso.")
            print()
            return True
        except Exception as e:
            print(f"❌ ERRO: {e}\n")
            return False