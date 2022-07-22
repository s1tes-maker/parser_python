from selenium.webdriver.common.by import By
from methods.sendReply import *



class AdvertisementsList:

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open_link(self):
        try:
            self.driver.get(url=self.url)
        except Exception as ex:
            send_reply("error", "can not open advertisement list page 0000002", str(ex.args[0]))

    def get_items_links(self):
        return self.driver.find_elements(By.CSS_SELECTOR, '[data-marker="item/link"]')

