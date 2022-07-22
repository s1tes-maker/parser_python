import methods
from sys import argv


def get_configs():
    script_name, process_id = argv
    connection = methods.connect()
    try:
        with connection.cursor() as cursor:
            query = "SELECT " \
                    "JSON_UNQUOTE(json_extract(avito_data, '$.url')) as url, " \
                    "JSON_UNQUOTE(json_extract(avito_data, '$.count')) as count, " \
                    "JSON_UNQUOTE(json_extract(avito_data, '$.suggest_price')) as suggest_price, " \
                    "JSON_UNQUOTE(json_extract(avito_data, '$.suggest_price_message')) as suggest_price_message, " \
                    "JSON_UNQUOTE(json_extract(avito_data, '$.discount_min')) as discount_min, " \
                    "JSON_UNQUOTE(json_extract(avito_data, '$.discount_max')) as discount_max " \
                    "FROM `configs` WHERE status='transfer_control_to_parser' AND process_id="+process_id
            cursor.execute(query)
            data = cursor.fetchone()
    except Exception as ex:
        print(": ошибка инициализации из config")
        print(ex)
        data_ret = 'error'
    else:
        if data is None:
            data_ret = False
        else:

            data_ret = {
                "url": data["url"],
                "count": int(data["count"]),

                "offer_price": {
                    "active": int(data["suggest_price"]),
                    "message": data["suggest_price_message"],
                    "discount_min": int(data["discount_min"]),
                    "discount_max": int(data["discount_max"])
                }
            }

    finally:
        connection.close()
    return data_ret
