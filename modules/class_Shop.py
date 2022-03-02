from .class_Browser import Browser, By
from .class_Text import Text
from .class_Logs import logger
from urllib import parse


class Shop(Browser):
    def __init__(self, url: str = ''):
        super().__init__()
        self.__url = url
        self.__domain = None

    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url

    @property
    def domain(self):
        self.__domain = Shop.domain_parser(self.url)
        return self.__domain

    @staticmethod
    def domain_parser(url):
        domain = parse.urlsplit(url).netloc
        if domain[0:3] == 'www':
            return domain[4:]
        return domain

    def check_market_or_no(self, normal_form_words: set):
        try:
            logger.OK('Connecting to', self.url)
            self.driver.get(self.url)
        except Exception as err:
            logger.FAIL('Connecting to', self.url, type(err))
            return False

        all_text = self.driver.find_element(By.TAG_NAME, 'body').text
        check = Text().word_matches(all_text, normal_form_words)
        if not check:
            logger.WARN('Website is not a market', self.url)
        return check

