def criar_personagem(id_usuario, nome_personagem, especie_personagem, cursor):
    if cursor:
        cursor.execute(f"SELECT f_cria_personagem({id_usuario}, '{nome_personagem}');")
        id_personagem = cursor.fetchone()['f_cria_personagem']
        # print(id_personagem)
        if id_personagem is None:
            print("❌ ERRO: Não foi possível criar personagem.")
            return False
        
        if especie_personagem == 'Zoiudo':
            cursor.execute(f"INSERT INTO public.ZOIUDO(id_personagem) VALUES ({id_personagem});")
        elif especie_personagem == 'Draconico':
            cursor.execute(f"INSERT INTO public.DRACONICO(id_personagem) VALUES ({id_personagem});")
        elif especie_personagem == 'Espiritualista':
            cursor.execute(f"INSERT INTO public.ESPIRITUALISTA(id_personagem) VALUES ({id_personagem});")
        elif especie_personagem == 'Titan':
            cursor.execute(f"INSERT INTO public.TITAN(id_personagem) VALUES ({id_personagem});")

        print(f"✅ Personagem criado com sucesso.")
        print()



