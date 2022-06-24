import parsing.avito.advertisement_item.methods.helpers as helpers
from parsing.mySelenium import MySelenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import random
import time


# чат с клиентом
class ChatForm(MySelenium):

    def __init__(self, driver, advert_data):
        super().__init__(driver)

        self.advert_data = advert_data
        self.msg_text = self.get_message()
        self.data_markers = {

            # кнопка Написать сообщение
            "open_chat_btn": '[data-marker="item-contact-bar/message"]',

            # инпут для вставки сообщения
            "input_msg": '[data-marker="reply/input"]',

            # кнопка Отправить сообщение
            "send_message_btn": '[data-marker="reply/send"]'
        }

    def open_chat_form(self):

        buttons = self.driver.find_elements(By.CSS_SELECTOR, self.data_markers["open_chat_btn"])

        if len(buttons) == 1:
            buttons[0].click()
            return True
        return False

    def get_message(self):
        buy_messages = helpers.get_message_chat()
        return random.choice(buy_messages).replace('%price%', str(self.advert_data["price"]))

    def put_message(self):

        WebDriverWait(self.driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, self.data_markers["input_msg"])))
        textarea = self.css_selector_one(self.data_markers["input_msg"])
        if textarea:
            textarea.send_keys(str(self.msg_text))

    def check_exists_id(self):
        return helpers.check_exists_id("chats", self.advert_data["advert_id"])

    def insert_msg_data(self):
        data = (
            self.advert_data["advert_id"],
            self.msg_text,
            self.advert_data["advert_url"])
        return helpers.insert_msg_data("chats", data)

    def send_message(self):
        send_btn = self.css_selector_one(self.data_markers["send_message_btn"])
        if send_btn:
            send_btn.click()

    def create_message(self):

        if self.open_chat_form():
            if self.check_exists_id() is False:
                self.put_message()
                self.insert_msg_data()
                self.send_message()
                time.sleep(5)
                return True
        return False
