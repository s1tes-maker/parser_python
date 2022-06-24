import warnings
import time

from parsing import avito, firefox
from methods.getConfigs import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

configs = get_configs()

advert_id = 1
msg_text = "text"
advert_url = "url"

# exit("test")
# пример обычного подключения
# url = "https://yandex.ru/internet"

# пример подключения Авито
# url = "https://www.avito.ru/moskva/kvartiry"
# url = "https://m.avito.ru/moskva/kvartiry/prodam-ASgBAgICAUSSA8YQ?context=H4sIAAAAAAAAA0u0MrSqLraysFJKK8rPDUhMT1WyBnOLM_KLSpJLS5SsawGw9bv_JAAAAA&radius=0&presentationType=serp"
# предложить свою цену
# url = "https://m.avito.ru/moskva/kvartiry/kvartira-studiya_17m_117et._2356702117?context=H4sIAAAAAAAA_0q0MrSqLrYytFKqULIutjI2tFKqNDUoLC5IzEpNLizKLSkxzi3NscgwTMo2NDNLyTPOUbKuBQQAAP__YwbUVzUAAAA"

#url = "https://m.avito.ru/moskva_i_mo/telefony?f=ASgCAgECAUXGmgwUeyJmcm9tIjoyMDAwLCJ0byI6MH0&geoCoords=55.755814%2C37.617635&radius=0&s=104&user=1&presentationType=serp"

# driver = avito.driver

profiles = ["xd474gbq.AvitoAB"]

Firefox = firefox.MyFirefox(profiles[0])
AvitoSelenium = avito.AvitoSelenium(Firefox)
driver = AvitoSelenium.driver

# driver.get(url)

# driver.quit()

# Firefox = firefox.MyFirefox(profiles[0])
# driver = Firefox.driver
# AvitoSelenium = avito.AvitoSelenium(Firefox)
# driver = AvitoSelenium.driver
# driver.get(url)
warnings.filterwarnings("ignore", category=DeprecationWarning)


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
                "bargain_message": False,
                "send_message": False,
                "chat": False,
                "price_interval": (41, 45)
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

            if i > ADVERT_AMOUNT - 1:
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
