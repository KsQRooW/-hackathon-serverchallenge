from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class Browser:
    def __init__(self):
        self.__options = webdriver.ChromeOptions()
        self.__options.add_argument('headless')
        self.__options.add_argument("–disable-infobars")
        self.__options.add_argument("–enable-automation")
        self.__options.add_argument("--disable-notifications")

        self.__driver = None
        self.__waiter = None

    def quit(self):
        self.__driver.quit()

    @property
    def driver(self):
        return self.__driver

    @driver.setter
    def driver(self, path):
        self.__driver = webdriver.Chrome(executable_path=path, options=self.__options)
        # self.__waiter = WebDriverWait(self.__driver, 5)

    @property
    def options(self):
        return self.__options

    def add_argument(self, arg: str):
        if isinstance(arg, str):
            self.__options.add_argument(arg)
        else:
            raise TypeError(f"Передан класс {type(arg)}. Ожидался класс str.")
