from .class_Browser import Browser
from .class_Text import Text, gost_inn
from .class_Logs import logger


class SpecificParsing(Browser):
    def __init__(self):
        super().__init__()
        self.general_url_spark = 'https://spark-interfax.ru/search?Query='

    def find_inn_by_url(self, site):
        url = self.general_url_spark + site
        self.get(url)
        list_items = self.html.find_all('li', class_='search-result-list__item')
        if len(list_items) == 0:
            return 0
        elif len(list_items) > 1:
            print('WARN: multiple results (', len(list_items), ')')
            item = list_items[0]            # TODO: Выбрать из нескольких результатов один
        else:
            item = list_items[0]
        data = item.find('div', class_='code').text.split()
        i = 0
        while i < len(data):
            if data[i] == 'ИНН':
                return data[i+1]
            i += 1
        return 0
