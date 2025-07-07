def equipar_item(cursor, id_instancia_item):
    try:
        cursor.execute(f"SELECT f_equipar_item({id_instancia_item});")
        cursor.connection.commit()
        print("✅ Item equipado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao equipar item: {e}")