from selenium.webdriver.common.by import By


class AdvertisementsList:

    def __init__(self, driver, url):
        self.driver = driver
        self.url = url

    def open_link(self):
        self.driver.get(url=self.url)

    def get_items_links(self):
        return self.driver.find_elements(By.CSS_SELECTOR, '[data-marker="item/link"]')

