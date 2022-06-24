from selenium.webdriver.common.by import By


class MySelenium:

    def __init__(self, driver):
        self.driver = driver

    def css_selector_one(self, selector):
        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
        if len(elements) > 0:
            return elements[0]
        return False

