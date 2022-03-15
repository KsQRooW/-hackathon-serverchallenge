from .class_Excel import Excel
from .class_Browser import Browser
from .class_Text import Text
from .class_SearchEngines import Google
from .class_Logs import Logs
from .class_Shop import Shop
from .config import *
from .class_Supplier import Supplier


# Парсинг и выгрузка экселя
excel_input_file = Excel(path_excel_input)
excel_input_line_number = excel_input_file.num_goods

text = Text()
# Загрузка словаря market_words
text.read_file(path_market_words)
text.normal_form()
market_words = text.word

# Загрузка словаря с типом юр. компаний
text.read_file(path_org_types)
org_types = text.word

# Инициализация браузера для работы с Google
google_browser = Google()
# google_browser.driver = path_web_driver

# Инициализация браузера для работы с магазинами
market_shop_browser = Shop()
# market_shop_browser.driver = path_web_driver

# Инициализация браузера для поиска информации по поставщику
supplier_browser = Supplier()

# Инициализация экселя для вывода
excel_file = Excel(path_excel_output, read_only=False)
