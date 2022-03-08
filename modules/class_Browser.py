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
        self.__headers = headers.copy()
        self.__headers.pop('Cookie')
        self.__proxies = proxies.copy()
        self.__html = BeautifulSoup()
        self.__domain_has = False
        self.__domain = None
        self.__url = None
        self.__cookie = None

    @property
    def cookie(self):
        return self.__cookie

    @cookie.setter
    def cookie(self, value):
        self.__cookie = value

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

    def __connect(self, url, time, google, verify):
        sleep(time)
        logger.INFO('Connecting to', url)
        response = requests.get(url=url, headers=self.__headers, timeout=(5, 5), verify=verify)
        if google:
            self.cookie = response.cookies
        response.raise_for_status()
        self.html = BeautifulSoup(response.text, 'lxml')

    def get(self, url, time=0, google=False):
        self.url = url
        if self.domain in Blacklist:
            logger.WARN('Website in Blacklist', self.url)
            return None
        try:
            self.__connect(url, time, google, True)
        except Exception as err:
            logger.WARN('Failed connect to', url, repr(err))
            try:
                self.__connect(url, time, google, False)
            except Exception as err:
                logger.FAIL('Not connected to', url, repr(err))
                return None
        return self.html
