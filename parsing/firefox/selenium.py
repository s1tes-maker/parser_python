from selenium.webdriver.firefox.service import Service as FirefoxService
from config import PATH_TO_GECKODRIVER, PATH_TO_FIREFOX, PATH_TO_PROFILES
from selenium import webdriver


class MyFirefox:

    def __init__(self, profile):

        self.connection_params = {
            "service_location": PATH_TO_GECKODRIVER,
            "browser_location": PATH_TO_FIREFOX,
            "user_agent": "default"
        }

        self.profile = profile
        self.driver = self.create_driver()

    def create_driver(self, user_agent=False):

        service = FirefoxService(self.connection_params["service_location"])

        options = webdriver.FirefoxOptions()
        options.headless = False
        profile = webdriver.FirefoxProfile()

        if user_agent:
            self.connection_params["user_agent"] = user_agent
            options.set_preference("general.useragent.override", self.connection_params["user_agent"])
            profile.set_preference("general.useragent.override", user_agent)

        options.profile = PATH_TO_PROFILES + self.profile
        options.binary_location = self.connection_params["browser_location"]

        self.driver = webdriver.Firefox(
            options=options,
            service=service
        )

        return self.driver
