from modules import excel_input_line_number, excel_input_file, market_words, google_browser, market_shop_browser, \
    params1, params2, num_google_pages, org_types
from pprint import pprint
from datetime import datetime


def main():
    items_and_shops = {}
    time = datetime.now()

    for i in range(excel_input_line_number):
        # Чтение одной строки из эксель файла
        current_item = excel_input_file.readline().structurizedata(params1, params2)
        # Три страницы поисковой выдачи
        pprint(current_item)
        for number in range(num_google_pages):
            google_browser.start_page = number
            google_browser.google_search(current_item['поиск'])
            # Получить список ссылок на данной странице гугл
            links_of_shops = google_browser.parse_google_links()

            for link in links_of_shops:
                # Проверка магазин ли это?
                if market_shop_browser.get(link):
                    if market_shop_browser.check_market_or_no(market_words):
                        """
                        # Проверка совпадения параметров из экселя с инф на сайте +++
                        if market_shop_browser.parameter_matching_excel(current_item['параметры']):
                            # парсинг ИНН
                                # парсинг инфы по магазину по ИНН
                                    # сохраняем магазин в словарь
                        """
                        # Проверка ГОСТа на сайте
                        if market_shop_browser.check_gost(current_item['параметры']['стандарт']):
                            # Парсинг ИНН
                            # descriptions = google_browser.parse_google_description()
                            # print(descriptions)
                            print(market_shop_browser.name_company_find(org_types))
                            if items_and_shops.get(current_item['поиск'], None):
                                items_and_shops[current_item['поиск']].add(market_shop_browser.url)
                            else:
                                items_and_shops.setdefault(current_item['поиск'], {market_shop_browser.url})

        # 7) ранжируем магазины для позиции из экселя
        # 8) выводим на отдельный лист экселя информацию по магазинам для товара

    pprint(items_and_shops)
    print(datetime.now() - time)

    excel_input_file.close_file()


if __name__ == '__main__':
    main()

# google_browser.quit()
# market_shop_browser.quit()
