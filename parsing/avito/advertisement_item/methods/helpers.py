import io
import methods


def get_message_chat():

    with io.open(r'C:\Users\1\PycharmProjects\pythonProject\parsing\avito\advertisement_item\methods\message_chat.txt', 'r',
                 encoding="utf-8") as f:
        return f.read().strip().split('\n\n')


def get_message_offer_price():

    with io.open(r'C:\Users\1\PycharmProjects\pythonProject\parsing\avito\advertisement_item\methods\offerprice_message.txt', 'r',
                 encoding="utf-8") as f:
        return f.read().strip().split('\n\n')


def check_exists_id(table, avito_id):
    connection = methods.connect()
    try:
        with connection.cursor() as cursor:
            query = "SELECT * FROM `" + table + "` WHERE avito_id = %s"
            cursor.execute(query, avito_id)
            data = cursor.fetchone()

    except Exception as ex:
        print(avito_id + ": ошибка поиска строки в БД ")
        print(ex)
        return_var = 'error'
    else:
        if data is None:
            return_var = False
        else:
            return_var = True
    finally:
        connection.close()
    return return_var


def insert_msg_data(table, data):
    connection = methods.connect()
    try:
        with connection.cursor() as cursor:
            insert_query = "INSERT INTO `" + table + "` (avito_id, text, url) VALUES (%s,%s,%s)"
            cursor.execute(insert_query, data)
            connection.commit()

    except Exception as ex:
        print(data["advert_id"] + ": ошибка записи в БД ")
        print(ex)
        return_var = False
    else:
        return_var = True
    finally:
        connection.close()
    return return_var

# поиск одинаковых записей
# FROM
# `chats`
# GROUP
# BY
# `avito_id`
# HAVING
# `count` > 1

