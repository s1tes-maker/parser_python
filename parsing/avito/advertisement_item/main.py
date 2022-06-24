from . import methods
from parsing.mySelenium import MySelenium
import time
import random


class AdvertisementItem(MySelenium):

    def __init__(self, params):
        super().__init__(params["driver"])
        self.url = params["advert_url"]
        self.send_message = params["send_message"] if "send_message" in params else False
        self.bargain_message = params["bargain_message"] if "bargain_message" in params else True

        self.price = None
        self.price_interval = params["price_interval"]

        self.id = None
        self.chat = params["chat"] if params["chat"] else False

        self.data_markers = {

            # всплывающее окно где тоже есть написать сообщение (удалить)
            "popup_contacts": '[data-marker="item-contact-bar/contacts-sticky"]',

            # если страница не найдена
            "page_not_found": '[data-marker="not-found"]',

            # объявление снято с публикации
            "page_advert_closed": '[data-marker^="item-closed"]',

            # поле содержащее id
            "avito_id": '[data-marker="item-stats/timestamp"]',

            # поле содержащее цену
            "advert_price": '[data-marker="item-description/price"]'
        }

        if self.page_exists() is True:

            self.get_price()
            self.get_id()

    def page_exists(self):

        not_found = self.css_selector_one(self.data_markers["page_not_found"])
        if not_found is not False:
            return False

        advert_closed = self.css_selector_one(self.data_markers["page_advert_closed"])

        if advert_closed is not False:
            return False

        return True

    def get_id(self):

        # номер объявы
        avito_id_elem = self.css_selector_one(self.data_markers["avito_id"])

        if avito_id_elem:
            self.id = avito_id_elem.text.replace('Объявление: №', '').split(',', 1)[0]

    def get_price(self):
        elem_price = self.css_selector_one(self.data_markers["advert_price"])

        if elem_price:
            self.price = float(elem_price.text.replace(' ', '').replace('₽', ''))

    def create_new_price(self):
        # print(self.price)

        price_proc = 1 - random.randint(self.price_interval[0], self.price_interval[1]) / 100
        # print(price_proc)
        # print(int(self.price * price_proc))
        return int(self.price * price_proc)

    def remove_popup(self):
        # удаляем всплывающее окно где тоже есть написать сообщение

        popup_contacts = self.css_selector_one(self.data_markers["popup_contacts"])
        if popup_contacts:
            self.driver.execute_script("""
                            var popup = arguments[0];
                            popup.parentNode.removeChild(popup);
                            """, popup_contacts)
        time.sleep(2)

    def suggest_price(self):
        if self.page_exists() is False:
            return False
        self.remove_popup()
        advert_data = {
            "advert_id": self.id,
            "price": self.create_new_price(),
            "advert_url": self.url,
            "send_message": self.send_message,
            "bargain_message": self.bargain_message
        }
        BargainForm = methods.BargainForm(self.driver, advert_data)
        return BargainForm.create_message()

    def create_message(self):
        if self.chat is False:
            return False
        if self.page_exists() is False:
            return False
        self.remove_popup()
        advert_data = {
            "advert_id": self.id,
            "price": self.create_new_price(),
            "advert_url": self.url
        }
        ChatForm = methods.ChatForm(self.driver, advert_data)
        if ChatForm.create_message():
            return True
        return False

