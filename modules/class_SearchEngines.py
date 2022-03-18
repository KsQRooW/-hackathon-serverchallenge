from .class_Browser import Browser
from .class_Logs import logger
from .class_Text import stop_extensions, inn, digits
from .config import headers
import re


class Google(Browser):
    def __init__(self):
        super().__init__()
        self.general_url = 'https://www.google.com/search?q='
        self.url = ''
        self.search = ''
        self.__start_page = 0
        self.__start = f"&start={self.start_page}0"
        self.__final_url = self.general_url + self.search + self.__start
        self.__description = ''
        self.__headers = headers.copy()

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, text):
        self.__description = text

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
        connect_url = self.general_url + self.search + self.__start

        # self.get(connect_url, time=2, google=True)
        self.get(connect_url, selen=True)
        # self.__headers['Cookie'] = self.cookie

    # метод поиска текста на сайте, используя встроенные средства Google
    # пример: google_search_text_on_site(ИНН, vk.com) -> запрос в Google: ИНН site:vk.com
    def google_search_inn_on_site(self, site_domain):
        connect_url = self.general_url + 'инн' + ' site%3A' + site_domain

        # self.get(connect_url, time=2, google=True)
        self.get(connect_url, selen=True)
        # self.__headers['Cookie'] = self.cookie

        self.parse_google_description()
        inns = re.findall(inn, self.description, flags=re.I)
        if not inns:
            return None
        inns_digits = tuple(map(lambda x: re.search(digits, x).group(), inns))
        inns_counts = set(map(lambda x: (x, inns.count(x)), inns_digits))
        max_inn = max(inns_counts, key=lambda x: x[1])[0]
        return max_inn  # Самый часто встрчаемый ИНН на странице

    # Парсинг ссылок с поискового запроса Google
    # Корректнее вызывать функцию после любой функции типа google_search...
    def parse_google_links(self) -> set:
        # url_pattern = re.compile(r'/url\?q=http.+')
        url_pattern = re.compile(r'http.+')
        classes_with_urls = self.html.find_all('a', {'href': url_pattern})
        markets_urls = set()
        for class_ in classes_with_urls:
            url = class_.get('href')
            clear_url = re.search(r'http.+', url).group()
            clear_url = re.split(r'&sa', clear_url)[0]
            if 'google' in clear_url:
                continue
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
                for div in divs[3:]:
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
