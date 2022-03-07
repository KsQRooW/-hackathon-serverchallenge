from .class_Browser import Browser
from .class_Text import Text, gost_inn
from .class_Logs import logger


class SpecificParsing(Browser):

    def __init__(self):
        super().__init__()
        self.website = ''

    def find_inn_by_url(self, site):
        logger.INFO('Start INN search by the site address', self.domain)
        self.website = site
        if self.__find_inn_spark():
            if len(self.inn) == 1:
                logger.INFO('INN found: ' + ' '.join(self.inn))     #TODO inn from list to int
            else:
                logger.WARN('Few INN found: ' + ' '.join(self.inn))
                self.__select_one_inn()
                logger.INFO('INN found: ' + ' '.join(self.inn))

    # Проверка, содержится ли домен site в списке urls
    @staticmethod
    def __is_right_url(urls, site):
        for temp in urls:
            if temp.get_text in (site, 'www.' + site):
                return True
        return False

    # Поиск ИНН по адресу сайта в базе данных spark-interfax.ru
    def __find_inn_spark(self):
        general_url = 'https://spark-interfax.ru/search?Query='
        self.inn = []
        url = general_url + self.website
        self.get(url)
        list_items = self.html.find_all('li', class_='search-result-list__item')
        if len(list_items) == 0:
            logger.FAIL('INN not found in database spark-interfax')
            return False
        else:
            for item in list_items:
                urls = item.find_all('span', class_='highlight')
                if self.__is_right_url(urls, self.website):
                    data = item.find('div', class_='code').get_text.split()
                    i = 0
                    while i < len(data):
                        if data[i] == 'ИНН':
                            self.inn.append(data[i + 1])
                        i += 1
                else:
                    logger.WARN('Wrong site', item.find('span', class_='highlight').get_text)    # debug
        return True

    def __select_one_inn(self):
        return True