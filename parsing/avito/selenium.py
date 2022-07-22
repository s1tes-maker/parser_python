from parsing import firefox


def create_driver(profile):
    Firefox = firefox.MyFirefox(profile)
    user_agent = "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36"
    # about:profiles

    Firefox.create_driver(user_agent)
    driver = Firefox.driver
    driver.set_window_size(600, 812)
    return driver

