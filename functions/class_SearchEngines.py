from .class_Browser import Browser, By
from .class_Logs import logger
from .class_Text import stop_extensions
import re


class Google(Browser):
    def google_links_parse(self, url: str) -> set:
        if not isinstance(url, str):
            return set()

        try:
            logger.OK('Connecting to', url)
            self.driver.get(url)
        except Exception as err:
            logger.FAIL('Connecting to', url, type(err))
            return set()

        classes_with_urls = self.driver.find_elements(By.CLASS_NAME, 'yuRUbf')
        markets_urls = set()
        for class_ in classes_with_urls:
            market_url = class_.find_element(By.TAG_NAME, 'a').get_attribute('href')
            check_stop_extensions = re.search(stop_extensions, market_url)
            if not check_stop_extensions:
                markets_urls.add(market_url)
            else:
                logger.WARNING(f"{check_stop_extensions.group()} file not a website", market_url)
        return markets_urls
