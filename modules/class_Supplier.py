from .class_Browser import Browser
from .class_Text import Text, inn
from .class_Logs import logger
from time import sleep
import re
from datetime import datetime


class Supplier(Browser):

    def __init__(self):
        super().__init__()
        self.__list_inn = []
        self.__inn = ''
        self.website = ''
        self.__supplier_data = {}

    @property
    def inn(self):
        return self.__inn

    @inn.setter
    def inn(self, inn):
        self.__inn = inn

    # Поиск ИНН по адресу сайта
    def find_inn_by_url(self, site):
        self.website = site
        self.__inn = ''
        logger.INFO('Start INN search by the site address', self.website)
        if self.__find_inn_spark():
            if len(self.__list_inn) == 1:
                self.__inn = self.__list_inn[0]
                logger.INFO('INN found: ' + self.inn)
            elif len(self.__list_inn) == 0:
                logger.FAIL('INN not found in database spark-interfax')
                return False
            else:
                logger.WARN('Few INN found: ' + ' '.join(self.__list_inn))
                self.__select_one_inn()
        return True

    # Проверка, содержится ли домен site в списке urls
    def __is_right_url(self, urls):
        for temp in urls:
            if self.get_text(temp) in (self.website, 'www.' + self.website):
                return True
        return False

    # Поиск ИНН по адресу сайта в базе данных spark-interfax.ru
    def __find_inn_spark(self):
        general_url = 'https://spark-interfax.ru/search?Query='
        self.__list_inn = []
        url = general_url + self.website
        self.get(url)
        list_items = self.html.find_all('li', class_='search-result-list__item')
        if len(list_items) == 0:
            logger.FAIL('INN not found in database spark-interfax')
            return False
        else:
            for item in list_items:
                urls = item.find_all('span', class_='highlight')
                if self.__is_right_url(urls):
                    data = self.get_text(item.find('div', class_='code')).split()
                    i = 0
                    while i < len(data):
                        if data[i] == 'ИНН':
                            self.__list_inn.append(data[i + 1])
                        i += 1
                else:
                    logger.WARN('Wrong site', self.get_text(item.find('span', class_='highlight')))    # debug
        return True

    def __select_one_inn(self):
        general_url = 'https://sbis.ru/contragents/'
        dates = {}
        logger.INFO('Search for the newest INN')
        for temp_inn in self.__list_inn:
            url = general_url + temp_inn
            self.get(url)
            # Проверка действующая ли компания или нет
            liquidated = self.get_text(self.html.find('div', class_='c-sbisru-CardStatus__closed'), log=False)
            if not liquidated:
                inf = self.get_text(self.html.find('div', class_='cCard__CompanyDescription'), log=False)
                try:
                    strdate = re.search(r'Действует с \d\d.\d\d.\d\d\d\d', inf).group()[12:]
                except Exception as er:
                    logger.FAIL('Date not found', err=repr(er))
                    continue
                dates[datetime.strptime(strdate, '%d.%m.%Y')] = temp_inn
            else:
                logger.WARN('INN ' + temp_inn + ' liquidated')
            sleep(1)                        # Pause to avoid ban
        if dates:
            self.__inn = dates[max(dates.keys())]
            logger.INFO('INN found: ' + self.inn)
            return True
        else:
            logger.FAIL('INN not found in database spark-interfax')
            return False

    @property
    def supplier_data(self):
        return self.__supplier_data

    def parse_supplier_data(self):
        self.__supplier_data = {}
        general_url = 'https://sbis.ru/contragents/'
        url = general_url + self.inn
        self.get(url, time=1)
        # Проверка действующая ли компания или нет
        liquidated = self.get_text(self.html.find('div', class_='c-sbisru-CardStatus__closed'), log=False)
        if liquidated:
            logger.FAIL('Supplier liquidated!')
            return False
        else:
            self.__supplier_data['Статус'] = 'Действующее'
            # Парсинг
            self.__supplier_data['ИНН'] = self.inn
            self.__supplier_data['Сайт'] = self.website
            # Дата регистрации
            inf = self.get_text(self.html.find('div', class_='cCard__CompanyDescription'), log=False)
            try:
                strdate = re.search(r'Действует с \d\d.\d\d.\d\d\d\d', inf).group()[12:]                    # TODO добавить КПП, ОГРН, ОКПО
            except Exception as er:
                logger.FAIL('Date not found', err=repr(er))
                strdate = ''
            self.__supplier_data['Дата регистрации'] = strdate
            #
            self.__supplier_data['Название'] = self.get_text(
                self.html.find('div', class_='cCard__MainReq-Name'), log=False
            )
            self.__supplier_data['Название полное'] = self.get_text(
                self.html.find('div', class_='cCard__MainReq-FullName'), log=False
            )
            self.__supplier_data['Руководитель'] = self.get_text(
                self.html.find('div', class_='cCard__Director-Name').find('span'), log=False
            ).strip()
            self.__supplier_data['Адрес'] = self.get_text(
                self.html.find('div', class_='cCard__Contacts-Address'), log=False
            ).strip()
            self.__supplier_data['Выручка'] = self.get_text(
                self.html.find(
                    'div', class_='cCard__Contacts'
                ).find(
                    'div', class_='cCard__Contacts-Revenue-Desktop cCard__Main-Grid-Element'
                ).find('span', class_='cCard__BlockMaskSum'),
                log=False
            ).strip()
            self.__supplier_data['Прибыль'] = self.get_text(
                self.html.find(
                    'div', class_='cCard__Owners-Profit-Desktop cCard__Main-Grid-Element'
                ).find('span', class_='cCard__BlockMaskSum'),
                log=False
            ).strip()
            # Суды
            try:
                self.__supplier_data['Истец'] = {}
                self.__supplier_data['Истец']['Выиграл'] = self.get_text(
                    self.html.find('div', class_='cCard__Owners-CourtStat-Complain').find(
                        'div', class_='cCard__Owners-CourtStat-Stat-Win'
                    ).find('div', class_='cCard__Owners-CourtStat-Stat-Value'),
                    log=False
                ).strip()
                self.__supplier_data['Истец']['Проиграл'] = self.get_text(
                    self.html.find('div', class_='cCard__Owners-CourtStat-Complain').find(
                        'div', class_='cCard__Owners-CourtStat-Stat-Loose'
                    ).find('div', class_='cCard__Owners-CourtStat-Stat-Value'),
                    log=False
                ).strip()
                self.__supplier_data['Истец']['Прочие'] = self.get_text(
                    self.html.find('div', class_='cCard__Owners-CourtStat-Complain').find(
                        'div', class_='cCard__Owners-CourtStat-Stat-Other'
                    ).find('div', class_='cCard__Owners-CourtStat-Stat-Value'),
                    log=False
                ).strip()
            except Exception:
                self.__supplier_data['Истец'] = ''
            #
            try:
                self.__supplier_data['Ответчик'] = {}
                self.__supplier_data['Ответчик']['Выиграл'] = self.get_text(
                    self.html.find('div', class_='cCard__Owners-CourtStat-Defend').find(
                        'div', class_='cCard__Owners-CourtStat-Stat-Win'
                    ).find('div', class_='cCard__Owners-CourtStat-Stat-Value'),
                    log=False
                ).strip()
                self.__supplier_data['Ответчик']['Проиграл'] = self.get_text(
                    self.html.find('div', class_='cCard__Owners-CourtStat-Defend').find(
                        'div', class_='cCard__Owners-CourtStat-Stat-Loose'
                    ).find('div', class_='cCard__Owners-CourtStat-Stat-Value'),
                    log=False
                ).strip()
                self.__supplier_data['Ответчик']['Прочие'] = self.get_text(
                    self.html.find('div', class_='cCard__Owners-CourtStat-Defend').find(
                        'div', class_='cCard__Owners-CourtStat-Stat-Other'
                    ).find('div', class_='cCard__Owners-CourtStat-Stat-Value'),
                    log=False
                ).strip()
            except Exception:
                self.__supplier_data['Ответчик'] = ''
            #
            self.__supplier_data['Уставный капитал'] = self.get_text(
                self.html.find(
                    'div', class_='cCard__Owners-OwnerList-Authorized-Capital-Sum cCard__Owners-OwnerList-Bold'
                ),
                log=False
            )
            self.__supplier_data['Стоимость'] = self.get_text(
                self.html.find(
                    'div', class_='cCard__Reliability-Cost-Desktop cCard__Main-Grid-Element'
                ).find('span', class_='cCard__BlockMaskSum'),
                log=False
            ).strip()
            # TODO Торги и госконтракты, Надежность, КПП, ОГРН

            # TODO отзывы
        return True

"""
Поиск ИНН по названию компании
https://sbis.ru/contragents
https://spark-interfax.ru/search
https://www.audit-it.ru/contragent/
https://www.kartoteka.ru/
https://www.list-org.com/search
https://classinform.ru/proverka-kontragenta.html
"""
