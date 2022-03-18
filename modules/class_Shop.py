from .class_Browser import Browser
from .class_Text import Text
from .class_Logs import logger


class Shop(Browser):
    # Проверка: является ли сайт магазином?
    # Проверка осуществляется с помощью парсинга текста с сайта, приведения слов к нормальной форме
    # и сопоставления со словами из собранного словаря market_words.txt
    # Если хоть одно слово с сайта есть в словаре - считаем, что этот сайт является магазином
    def check_market_or_no(self, normal_form_words: set) -> bool:
        all_text = self.get_text(self.html.find('body'))

        check = Text().word_matches(all_text, normal_form_words)
        if not check:
            logger.WARN('Website is not a market', self.url)
        return check

    # Проверка: есть ли необходимый ГОСТ на странице магазина с товаром?
    # Парсится весь текст со страницы с товаром, с помощью регулярных выражений ищутся все ГОСТы на странице
    # и их номера, происходит сопоставления ГОСТа и его номера с Excel файла искомого товара с ГОСТами
    # на странице товара в магазине
    def check_gost(self, parameters):
        all_text = self.get_text(self.html.find('body'))

        check = Text().gost_check(all_text.lower(), parameters.lower())
        if not check:
            logger.WARN('GOST not found', self.url)
        return check

    # Поиск названия компании с их страницы при помощи регулярных выражений
    def name_company_find(self, org_types: set):
        all_text = self.get_text(self.html.find('body'))

        name = Text().name_find(all_text.lower(), org_types)
        return name
