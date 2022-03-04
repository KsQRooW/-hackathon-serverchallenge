headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9 '
}

proxies = {
            'http': 'http://185.174.138.19:80',  # http Russia - 20ms
            'https': 'https://91.224.62.194:8080'  # https Russia - 20ms
}

path_excel_input = 'source/poiskpostav_v1.xlsx'                 # Список товаров

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

Blacklist = {
    'docs.cntd.ru',
    'gost.ru',
    'gostinfo.ru',
    'standards.ru',
    'docplayer.com',
    'terracompozit.ru'
}

# driver = ChromeDriverManager().install()
