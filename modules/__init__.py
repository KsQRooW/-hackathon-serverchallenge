from .class_Excel import Excel
from .class_Browser import Browser
from .class_Text import Text
from .class_SearchEngines import Google
from .class_Logs import Logs
from .class_Shop import Shop
from .config import *
from .class_SpecificParsing import SpecificParsing


# Парсинг и выгрузка экселя
excel_input_file = Excel(path_excel_input)
excel_input_line_number = excel_input_file.num_goods
# excel_input_file.importgoods()
# excel_input_data = excel_input_file.structurizedata(params1, params2)

# Загрузка словаря market_words
words_cleaner = Text()
words_cleaner.read_file(path_market_words)
words_cleaner.normal_form()
market_words = words_cleaner.word

# Инициализация браузера для работы с Google
google_browser = Google()
# google_browser.driver = path_web_driver

# Инициализация браузера для работы с магазинами
market_shop_browser = Shop()
# market_shop_browser.driver = path_web_driver

# Инициализация браузера для поиска информации по поставщику
supplier_browser = SpecificParsing()
