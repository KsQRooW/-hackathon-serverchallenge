from .class_Browser import Browser
from .class_Text import Text, gost_inn
from .class_Logs import logger


class Shop(Browser):
    def check_market_or_no(self, normal_form_words: set) -> bool:
        try:
            all_text = self.html.find('body').text
        except Exception as err:
            logger.FAIL('Text not found', self.url, repr(err))
            all_text = ''

        check = Text().word_matches(all_text, normal_form_words)
        if not check:
            logger.WARN('Website is not a market', self.url)
        return check

    def check_gost(self, parameters):
        try:
            all_text = self.html.find('body').text
        except Exception as err:
            logger.FAIL('Text not found', self.url, repr(err))
            all_text = ''

        check = Text().reg_find(all_text, parameters)
        if not check:
            logger.WARN('GOST not found', self.url)
        return check
