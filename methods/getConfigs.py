import methods


def get_configs():
    connection = methods.connect()
    try:
        with connection.cursor() as cursor:
            query = "SELECT url, count FROM `configs`"
            cursor.execute(query)
            data = cursor.fetchone()

    except Exception as ex:
        print(": ошибка инициализации из config ")
        print(ex)
        return_var = 'error'
    else:
        if data is None:
            return_var = False
        else:
            return_var = data
    finally:
        connection.close()
    return return_var
