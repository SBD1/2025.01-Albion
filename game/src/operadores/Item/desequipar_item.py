def desequipar_item(cursor, id_instancia_item):
    try:
        cursor.execute(f"SELECT f_desequipar_item({id_instancia_item});")
        cursor.connection.commit()
        print("✅ Item desequipado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao desequipar item: {e}")