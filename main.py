from modules import excel_input_line_number, excel_input_file, market_words, google_browser, market_shop_browser, \
    params1, params2, num_google_pages, supplier_browser
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
                        # Проверка совпадения параметров из экселя с инф на сайте
                        # Проверка ГОСТа на сайте
                        if market_shop_browser.check_gost(current_item['параметры']['стандарт']):
                            # Парсинг ИНН
                            inn = google_browser.google_search_inn_on_site(market_shop_browser.domain)
                            if inn:
                                supplier_browser.inn = inn
                            else:
                                if not supplier_browser.find_inn_by_url(market_shop_browser.domain):    # Поиск ИНН по адресу сайта
                                    continue
                            # Парсинг информации по поставщику
                            if supplier_browser.parse_supplier_data():
                                # Сохранение информации по поставщику
                                # TODO сохранение из supplier_browser.supplier_data
                                pprint(supplier_browser.supplier_data)
                                # TODO add market_shop_browser.url
                                if items_and_shops.get(current_item['поиск'], None):
                                    items_and_shops[current_item['поиск']].add((market_shop_browser.url, supplier_browser.inn))
                                else:
                                    items_and_shops.setdefault(current_item['поиск'], {(market_shop_browser.url, supplier_browser.inn)})

        # 7) ранжируем магазины для позиции из экселя
        # 8) выводим на отдельный лист экселя информацию по магазинам для товара

    pprint(items_and_shops)
    print(datetime.now() - time)

    excel_input_file.close_file()


if __name__ == '__main__':
    main()

# google_browser.quit()
# market_shop_browser.quit()
