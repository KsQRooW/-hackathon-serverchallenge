from urllib import parse
from .config import headers, proxies, Blacklist
from .class_Logs import logger
import requests
from bs4 import BeautifulSoup
from time import sleep
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class Browser:
    def __init__(self):
        self.__headers = headers
        self.__proxies = proxies
        self.__html = BeautifulSoup()
        self.__domain_has = False
        self.__domain = None
        self.__url = None

    @property
    def domain_has(self):
        return self.__domain_has

    @domain_has.setter
    def domain_has(self, value: bool):
        if not isinstance(value, bool):
            raise TypeError(f"Передан класс {type(value)}. Ожидался класс Bool.")
        self.__domain_has = value

    @staticmethod
    def get_text(item, log=True):
        try:
            all_text = item.text
        except Exception as err:
            if log:
                logger.FAIL('Text not found', item.url, repr(err))
            all_text = ''
        return all_text

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url
        self.domain_has = False

    @property
    def domain(self):
        if not self.url:
            raise Exception("URL is None type. Use .get or .url")
        if not self.domain_has:
            self.__domain = self.domain_parser(self.url)
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
            response = requests.get(url=url, headers=self.__headers, timeout=(5, 5))
            sleep(2)
            response.raise_for_status()
            self.html = BeautifulSoup(response.text, 'lxml')
        except Exception as err:
            logger.WARN('Failed connect to', url)
            try:
                logger.INFO('Reconnecting to', url)
                response = requests.get(url=url, headers=self.__headers, timeout=(5, 5), verify=False)
                sleep(2)
                response.raise_for_status()
                self.html = BeautifulSoup(response.text, 'lxml')
            except Exception as err:
                logger.FAIL('Not connected to', url, repr(err))
                return None
        return self.html
