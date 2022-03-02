from .class_Browser import Browser, By
from .class_Logs import logger
from .class_Text import stop_extensions
import re


class Google(Browser):
    def __init__(self):
        super().__init__()
        self.__url = 'https://www.google.com/search?q='
        self.search = ''
        self.__start_page = 0
        self.__start = f"&start={self.start_page}0"
        self.__final_url = self.__url + self.search + self.__start

    @property
    def url(self):
        return self.__url

    # Вернуть номер стартовой страницы
    @property
    def start_page(self):
        return self.__start_page

    # Указать номер стартовой страницы поискового запроса Google
    @start_page.setter
    def start_page(self, number: int):
        if not isinstance(number, int):
            raise TypeError(f"Передан класс {type(number)}. Ожидался класс int.")
        self.__start_page = number
        self.__start = f"&start={self.start_page}0"

    # Отправка поискового запроса в Google
    def google_search(self, text):
        self.search = text
        connect_url = self.url + self.search + self.__start
        try:
            logger.OK('Connecting to', connect_url)
            self.driver.get(connect_url)
        except Exception as err:
            logger.FAIL('Connecting to', connect_url, type(err))

    # метод поиска текста на сайте, используя встроенные средства Google
    # пример: google_search_text_on_site(ИНН, vk.com) -> запрос в Google: ИНН site:vk.com
    def google_search_text_on_site(self, text, site_domain):
        connect_url = self.url + text + 'site%3A' + site_domain
        try:
            logger.OK('Connecting to', connect_url)
            self.driver.get(connect_url)
        except Exception as err:
            logger.FAIL('Connecting to', connect_url, type(err))

    # Парсинг ссылок с поискового запроса Google
    # Корректнее вызывать функцию после любой функции типа google_search...
    def google_links_parse(self) -> set:
        classes_with_urls = self.driver.find_elements(By.CLASS_NAME, 'yuRUbf')
        markets_urls = set()
        for class_ in classes_with_urls:
            market_url = class_.find_element(By.TAG_NAME, 'a').get_attribute('href')
            check_stop_extensions = re.search(stop_extensions, market_url)
            if not check_stop_extensions:
                markets_urls.add(market_url)
            else:
                logger.WARN(f"{check_stop_extensions.group()} file not a website", market_url)
        return markets_urls
