from .class_Browser import Browser
from .class_Text import Text
from .class_Logs import logger
from .config import Blacklist


class Shop(Browser):
    def __init__(self, url: str = ''):
        super().__init__()

    def check_market_or_no(self, normal_form_words: set) -> bool:
        if not self.get(self.url):
            return False
        # all_text = self.driver.find_element(By.TAG_NAME, 'body').text
        try:
            all_text = self.html.find('body').text
        except Exception as err:
            logger.FAIL('Text not found', self.url, repr(err))
            all_text = ''

        check = Text().word_matches(all_text, normal_form_words)
        if not check:
            logger.WARN('Website is not a market', self.url)
        return check
