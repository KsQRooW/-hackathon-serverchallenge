from .class_Browser import Browser
from .class_Logs import logger
from .class_Text import stop_extensions
import re


class Google(Browser):
    def __init__(self):
        super().__init__()
        self.url = 'https://www.google.com/search?q='
        self.search = ''
        self.__start_page = 0
        self.__start = f"&start={self.start_page}0"
        self.__final_url = self.url + self.search + self.__start
        self.__description = ''

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, text):
        self.description += text

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
        self.get(connect_url)

        # try:
        #     logger.OK('Connecting to', connect_url)
        #     self.driver.get(connect_url)
        # except Exception as err:
        #     logger.FAIL('Connecting to', connect_url, type(err))

    # метод поиска текста на сайте, используя встроенные средства Google
    # пример: google_search_text_on_site(ИНН, vk.com) -> запрос в Google: ИНН site:vk.com
    def google_search_text_on_site(self, text, site_domain):
        connect_url = self.url + text + 'site%3A' + site_domain
        self.get(connect_url)

        # try:
        #     logger.OK('Connecting to', connect_url)
        #     self.driver.get(connect_url)
        # except Exception as err:
        #     logger.FAIL('Connecting to', connect_url, type(err))

    # Парсинг ссылок с поискового запроса Google
    # Корректнее вызывать функцию после любой функции типа google_search...
    def parse_google_links(self) -> set:
        url_pattern = re.compile(r'/url\?q=http.+')
        classes_with_urls = self.html.find_all('a', {'href': url_pattern})
        # classes_with_urls = self.driver.find_elements(By.CLASS_NAME, 'yuRUbf')
        markets_urls = set()
        for class_ in classes_with_urls:
            url = class_.get('href')
            clear_url = re.search(r'http.+', url).group()
            clear_url = re.split(r'&sa', clear_url)[0]
            if 'google' in clear_url:
                continue
            # market_url = class_.find_element(By.TAG_NAME, 'a').get_attribute('href')
            check_stop_extensions = re.search(stop_extensions, clear_url)
            if not check_stop_extensions:
                markets_urls.add(clear_url)
            else:
                logger.WARN(f"{check_stop_extensions.group()} file not a website", clear_url)
        return markets_urls

    def __recursion_find(self, s, check=True):
        divs = s.find_all('div', recursive=False)
        if divs:
            if check:  # Для первого прохода по div'ам
                for div in divs[3:-1]:
                    if div.find_all_next('a'):
                        self.__recursion_find(div, False)
            else:
                for div in divs:
                    if div.find_all_next('a'):
                        self.__recursion_find(div, False)
        elif s.find_previous('div').find('a', recursive=False) is None:
            self.description += s.text + ' '

    def parse_google_description(self):
        self.description = ''
        divs = self.html.find('body').find('div', {'id': 'main'})
        self.__recursion_find(divs)
        return self.description

    """
    def parse_google_description(self):
        self.description = ''
        divs = self.html.find('div', id='main').find_all('div', class_='BNeawe s3v9rd AP7Wnd')
        for div in divs:
            if div.next.name is None:
                self.description += div.text + ' '
    """
