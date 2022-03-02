path_excel_input = 'source/poiskpostav_v1_test.xlsx'                 # Список товаров

path_market_words = 'source/market_words.txt'

path_web_driver = 'source/chromedriver.exe'

params1 = {'стандарт': 'ГОСТ',                      # Параметры товаров 1 типа
           'покрытие': 'покрытие',
           'головка': 'головка',
           'рабочий вакуум': 'рабочий вакуум'
           }

num_google_pages = 3                                # Количество страниц в поиске гугл

params2 = {'СТАНДАРТ', 'ГОЛОВКА', 'ОБОЗНАЧЕНИЕ',    # Параметры товаров 2 типа
           'КЛАСС ПРОЧНОСТИ', 'МАТЕРИАЛ', 'ТИП'
           }

# driver = ChromeDriverManager().install()
