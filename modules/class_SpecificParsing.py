from .class_Browser import Browser
from .class_Text import Text, gost_inn
from .class_Logs import logger


class SpecificParsing(Browser):

    # Проверка, содержится ли домен site в списке urls
    @staticmethod
    def __is_right_url(urls, site):
        for temp in urls:
            if temp.text in (site, 'www.' + site):
                return True
        return False

    # Поиск ИНН по адресу сайта в базе данных spark-interfax.ru
    def find_inn_by_url(self, site):
        general_url = 'https://spark-interfax.ru/search?Query='
        inn = []
        url = general_url + site
        self.get(url)
        list_items = self.html.find_all('li', class_='search-result-list__item')
        if len(list_items) == 0:
            logger.FAIL('INN not found in database spark-interfax')
            return inn
        else:
            for item in list_items:
                urls = item.find_all('span', class_='highlight')
                if self.__is_right_url(urls, site):
                    data = item.find('div', class_='code').text.split()
                    i = 0
                    while i < len(data):
                        if data[i] == 'ИНН':
                            inn.append(data[i + 1])
                        i += 1
                else:
                    logger.WARN('Wrong site', item.find('span', class_='highlight').text)    # debug
        return inn
