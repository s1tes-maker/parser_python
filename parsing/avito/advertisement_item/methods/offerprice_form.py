from selenium.webdriver.common.by import By
from parsing.mySelenium import MySelenium
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from . import helpers
import random
import time


# форма Предложить свою цену
class OfferPriceForm(MySelenium):

    def __init__(self, driver, advert_data):
        super().__init__(driver)
        self.advert_data = advert_data
        self.msg_text = self.get_message()
        self.data_markers = {
            "open_offer_price_form": '[data-marker="bargain-offer/show-button"]',
            "input_price": '[data-marker="bargain-offer/form-price"]',
            "input_msg": '[data-marker="bargain-offer/form-message"]',
            "send_message_btn": '[data-marker="bargain-offer/form-submit"]'
        }

    def open_offer_price_form(self):
        offer_price_btn = self.css_selector_one(self.data_markers["open_offer_price_form"])

        if offer_price_btn:
            offer_price_btn.click()
            return True
        return False

    def suggest_price(self):

        input_price = self.css_selector_one(self.data_markers["input_price"])

        if input_price:
            if int(self.advert_data["price"]) > 0:
                input_price.send_keys(str(self.advert_data["price"]))
                return True
        return False

    def get_message(self):
        if "offer_price_message" in self.advert_data:
            if self.advert_data["offer_price_message"] is False:
                return ""
        buy_messages = helpers.get_message_offer_price()
        return random.choice(buy_messages)

    def put_message(self):
        if self.advert_data["offer_price_message"] is False:
            return
        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.data_markers["input_price"])))
        textarea = self.css_selector_one(self.data_markers["input_msg"])
        if textarea:
            textarea.send_keys(str(self.msg_text))

    def check_exists_id(self):
        return helpers.check_exists_id("suggest_prices", self.advert_data["advert_id"])

    def insert_msg_data(self):
        data = (
            self.advert_data["advert_id"],
            self.msg_text,
            self.advert_data["advert_url"])
        return helpers.insert_msg_data("suggest_prices", data)

    def send_message(self):
        if self.advert_data["send_message"] is False:
            return
        send_btn = self.css_selector_one(self.data_markers["send_message_btn"])
        if send_btn:
            send_btn.click()

    def close_offer_price_form(self):
        close = self.driver.find_elements(By.CLASS_NAME, "NqV6X")
        if len(close) > 0:
            close[0].click()

    def create_message(self):

        if self.open_offer_price_form():
            if self.check_exists_id() is False:
                self.suggest_price()
                self.put_message()
                self.insert_msg_data()
                self.send_message()
                time.sleep(3)

                return True
            else:
                return "sent"
        return False
