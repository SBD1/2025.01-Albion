def visualizar_personagens(id_usuario,cursor):
    
    cursor.execute(f"""
SELECT 
    p.id_personagem,
    p.nome, 
    p.nivel, 
    p.qtd_ouro, 
    CASE 
        WHEN z.id_personagem IS NOT NULL THEN 'Zoiudo'
        WHEN e.id_personagem IS NOT NULL THEN 'Espiritualista'
        WHEN d.id_personagem IS NOT NULL THEN 'Draconico'
        WHEN t.id_personagem IS NOT NULL THEN 'Titan'
        ELSE 'Desconhecido'
    END AS especie
FROM public.personagem p
    LEFT JOIN public.zoiudo z ON p.id_personagem = z.id_personagem
    LEFT JOIN public.espiritualista e ON p.id_personagem = e.id_personagem
    LEFT JOIN public.draconico d ON p.id_personagem = d.id_personagem
    LEFT JOIN public.titan t ON p.id_personagem = t.id_personagem
WHERE 
    p.id_usuario = {id_usuario};""")

    rows = cursor.fetchall()
    # print(resultado)
    if rows is None:
        print("Nenhum personagem encontrado.")
        return None
    else:
        return rows

    