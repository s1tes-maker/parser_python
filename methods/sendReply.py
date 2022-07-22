import methods
from sys import argv
import logging


def send_reply(status, message, error_log=False):
    script_name, process_id = argv
    if error_log:
        logging.basicConfig(filename="error.log")
        logging.error('process:' + process_id + ' ' + message + ' ' + error_log)
    connection = methods.connect()
    try:
        with connection.cursor() as cursor:
            update_query = "UPDATE `configs` " \
                           "SET status=%s, python_message=%s" \
                           "WHERE process_id="+process_id
            cursor.execute(update_query, (status, message))
            connection.commit()

    except Exception as ex:
        print("Process_id " + process_id + ": ошибка записи в БД ")
        print(ex)
        return_var = False
    else:
        return_var = True
    finally:
        connection.close()
    return return_var
