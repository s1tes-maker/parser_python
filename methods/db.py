import pymysql
import pymysql.cursors
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_DATABASE


def connect():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_DATABASE,
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as ex:
        print("Не удалось установить соединение с БД")
        print(ex)
        return False
    return connection
