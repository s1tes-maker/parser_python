import methods
import json


def get_configs():
    connection = methods.connect()
    try:
        with connection.cursor() as cursor:
            query = "SELECT " \
                    "avito_data->>'$.url' AS url, " \
                    "avito_data->>'$.count' AS count, " \
                    "avito_data->>'$.suggest_price' AS suggest_price, " \
                    "avito_data->>'$.suggest_price_message' AS suggest_price_message, " \
                    "avito_data->>'$.discount_min' AS discount_min, " \
                    "avito_data->>'$.discount_max' AS discount_max " \
                    "FROM `configs` WHERE processing is NULL ORDER BY id DESC"
            cursor.execute(query)
            data = cursor.fetchone()

    except Exception as ex:
        print(": ошибка инициализации из config")
        print(ex)
        return_var = 'error'
    else:
        if data is None:
            return_var = False
        else:

            data_ret = {
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
