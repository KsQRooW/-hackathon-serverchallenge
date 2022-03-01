from functions import excel_input_data, market_words, google_browser, market_shop_browser
from pprint import pprint
from datetime import datetime


products_and_shops = {}
time = datetime.now()

for element in excel_input_data:
    # 0) парсинг одной строки из экселя

    for number in range(3):
        google_link = 'https://www.google.com/search?q=' + element['поиск'] + f"&start={number}0"
        links_of_shops = google_browser.google_links_parse(google_link)

        for link in links_of_shops:

            # 1) проверка магазин ли это?
            # 2) домашний адресс
            # 3) проверка сравнить параметры с экселем?
            # 4) парсинг ИНН для сайта
            # 5) парсинг инфы по магазину по ИНН
            # 6) сохраняем магазин

            market_shop_browser.url = link
            if market_shop_browser.check_market_or_no(market_words):
                if products_and_shops.get(element['поиск'], None):
                    products_and_shops[element['поиск']].add(market_shop_browser.domain)
                else:
                    products_and_shops.setdefault(element['поиск'], {market_shop_browser.domain})


        # 7) ранжируем магазины для позиции из экселя
        # 8) выводим на отдельный лист экселя информацию по магазинам для товара

pprint(products_and_shops)
print(datetime.now() - time)

google_browser.quit()
market_shop_browser.quit()
