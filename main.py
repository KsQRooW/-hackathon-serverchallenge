from functions import structuredData, driver
from functions.parse_google_search import *
from pprint import pprint
# from datetime import datetime

# start_time = datetime.now()
# print(start_time)
# print('-' * 15)

# pprint(structuredData)
# print('-' * 15)

market_words = market_words_creater('source/market_words.txt')

products_and_shops = {}
for element in structuredData:

    google_link = 'https://www.google.com/search?q=' + element['поиск']
    links_of_shops = google_links_parse(driver, google_link)

    # pprint(links_of_shops)
    # print('-' * 15)

    for link in links_of_shops:
        if check_market_or_no(driver, link, market_words, MorphAnalyzer()):
            if products_and_shops.get(element['поиск'], None):
                products_and_shops[element['поиск']].add(link)
            else:
                products_and_shops.setdefault(element['поиск'], {link})

    # print(datetime.now() - start_time)
    # print('-' * 15)

pprint(products_and_shops)
