from urllib import parse
from .config import headers, proxies, Blacklist
from .class_Logs import logger
# from selenium import webdriver
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Browser:
    def __init__(self):
        self.__headers = headers
        self.__proxies = proxies
        self.__html = BeautifulSoup()
        self.__domain = None
        self.__url = None

        # self.__requests = requests
        # self.__BeautifulSoup = BeautifulSoup

        # self.__options = webdriver.ChromeOptions()
        # self.__options.add_argument('headless')
        # self.__options.add_argument("–disable-infobars")
        # self.__options.add_argument("–enable-automation")
        # self.__options.add_argument("--disable-notifications")
        #
        # self.__driver = None
        # self.__waiter = None

    """
    @property
    def BeautifulSoup(self):
        return self.__BeautifulSoup

    @property
    def requests(self):
        return self.__requests
    """
    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    @property
    def domain(self):
        self.__domain = Browser.domain_parser(self.url)
        return self.__domain

    @staticmethod
    def domain_parser(url):
        domain = parse.urlsplit(url).netloc
        if domain[0:3] == 'www':
            return domain[4:]
        return domain

    @property
    def html(self):
        return self.__html

    @html.setter
    def html(self, soup):
        if not isinstance(soup, BeautifulSoup):
            raise TypeError(f"Передан класс {type(soup)}. Ожидался класс BeautifulSoup.")
        self.__html = soup

    def html_clear(self):
        self.html = ''

    def get(self, url):
        self.url = url
        if self.domain in Blacklist:
            logger.WARN('Website in Blacklist', self.url)
            return None
        try:
            logger.INFO('Connecting to', url)
            # (proxies=proxies)
            # timeout=(5, 5) - Время на коннект и чтение страницы соответственно
            response = requests.get(url=url, headers=self.__headers, timeout=(5, 5))
            self.html = BeautifulSoup(response.text, 'lxml')
        except Exception as err:
            logger.WARN('Failed connect to', url)
            try:
                logger.INFO('Reconnecting to', url)
                # (proxies=proxies)
                response = requests.get(url=url, headers=self.__headers, timeout=(5, 5), verify=False)
                self.html = BeautifulSoup(response.text, 'lxml')
            except Exception as err:
                logger.FAIL('Not connected to', url, repr(err))
                return None
        return self.html

    """
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
    """
