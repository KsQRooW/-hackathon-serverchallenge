from .class_Browser import Browser
from .class_Text import Text
from .class_Logs import logger


class Shop(Browser):
    def check_market_or_no(self, normal_form_words: set) -> bool:
        all_text = self.text(self.html.find('body'))

        check = Text().word_matches(all_text, normal_form_words)
        if not check:
            logger.WARN('Website is not a market', self.url)
        return check

    def check_gost(self, parameters):
        all_text = self.text(self.html.find('body'))

        check = Text().gost_inn_find(all_text.lower(), parameters.lower())
        if not check:
            logger.WARN('GOST not found', self.url)
        return check

    def name_company_find(self, org_types: set):
        all_text = self.text(self.html.find('body'))

        name = Text().name_find(all_text.lower(), org_types)
        return name
