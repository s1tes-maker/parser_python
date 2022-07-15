import time
from parsing import avito, firefox
from methods.getConfigs import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from sys import argv

# пример обычного подключения
# url = "https://yandex.ru/internet"
# пример подключения Авито
# url = "https://m.avito.ru/moskva_i_mo/telefony?f=ASgCAgECAUXGmgwUeyJmcm9tIjoyMDAwLCJ0byI6MH0&geoCoords=55.755814%2C37.617635&radius=0&s=104&user=1&presentationType=serp"
process_id = argv
exit(process_id)
configs = get_configs()

if configs["offer_price"]["active"] != 1:
    exit("Программа успешно выполнена. Обработано объявлений 0")

profiles = ["xd474gbq.AvitoAB"]

Firefox = firefox.MyFirefox(profiles[0])
AvitoSelenium = avito.AvitoSelenium(Firefox)
driver = AvitoSelenium.driver

try:

    AdvertisementsList = avito.advertisments_list.AdvertisementsList(driver, configs["url"])
    AdvertisementsList.open_link()

    i = 0
    last_link = False
    while i < configs["count"]:
        links = AdvertisementsList.get_items_links()
        flag: str = "continue"

        print(i)
        for link in links:
            if link != last_link and last_link is not False and flag != "stop":
                if flag == "continue":
                    continue
            else:
                flag = "stop"
            time.sleep(5)
            advert_url = link.get_attribute('href')
            driver.execute_script("arguments[0].scrollIntoView();", link)
            original_window = driver.current_window_handle
            driver.switch_to.new_window('tab')
            driver.get(advert_url)
            time.sleep(2)

            AdvertisementItem = avito.advertisement_item.AdvertisementItem({
                "driver": driver,
                "advert_url": advert_url,
                "offer_price_message": False,
                "send_message": False,
                "chat": False,
                "price_interval": (configs["discount_min"], configs["discount_max"])
            })

            suggest_price = AdvertisementItem.suggest_price()
            if suggest_price is True:
                i = i + 1
            else:
                if suggest_price != "sent":
                    if AdvertisementItem.create_message():
                        i = i + 1

            driver.close()
            driver.switch_to.window(original_window)

            if i > configs["count"] - 1:
                break

            last_link = link
        # print(i)
        time.sleep(10)
        html = driver.find_element(by=By.TAG_NAME, value="html")
        html.send_keys(Keys.END)

        else_btn = driver.find_elements(by=By.CLASS_NAME, value="TWHkq")
        if len(else_btn) > 0:
            else_btn[0].click()
            # last_link = False

        time.sleep(5)

    time.sleep(5)

except Exception as ex:
    print(ex)
