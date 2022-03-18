from modules import excel_input_line_number, excel_input_file, market_words, google_browser, market_shop_browser, \
    excel_params1, excel_params2, num_google_pages, supplier_browser, org_types, excel_output_file
from pprint import pprint
from datetime import datetime


def main():
    items_and_shops = {}
    time = datetime.now()

    # output = open('source/output.txt', 'w', encoding='utf-8')
    for i in range(3):
        # Чтение одной строки из эксель файла
        current_item = excel_input_file.readline().structurizedata(excel_params1, excel_params2)

        markets_ranked = []

        # Три страницы поисковой выдачи
        pprint(current_item)

        # Получить список ссылок на текущей странице гугл
        links_of_shops = set()
        with open(file=f'files_for_tests/market_links_{i + 1}.txt', mode='r', encoding='utf-8') as links:
            for j in links:
                links_of_shops.add(j.rstrip())

        for link in links_of_shops:
            # Проверка магазин ли это?
            if market_shop_browser.get(link):
                if market_shop_browser.check_market_or_no(market_words):
                    # Проверка совпадения параметров из экселя с инф на сайте
                    # Проверка ГОСТа на сайте
                    if market_shop_browser.check_gost(current_item['параметры']['стандарт']):
                        # Парсинг ИНН
                        inn = google_browser.google_search_inn_on_site(market_shop_browser.domain) # Google
                        # inn = False
                        if inn:
                            supplier_browser.inn = inn
                        else:
                            # Поиск ИНН по адресу сайта
                            if not supplier_browser.find_inn_by_url(market_shop_browser.domain):
                                continue
                        # Парсинг информации по поставщику
                        if supplier_browser.parse_supplier_data():
                            # pprint(supplier_browser.supplier_data)
                            # Присвоения ранга магазину
                            supplier_browser.ranking()
                            markets_ranked.append(supplier_browser.supplier_data)
                            if items_and_shops.get(current_item['поиск'], None):
                                items_and_shops[current_item['поиск']].add(
                                    (market_shop_browser.url, supplier_browser.inn))
                            else:
                                items_and_shops.setdefault(current_item['поиск'],
                                                           {(market_shop_browser.url, supplier_browser.inn)})
        markets_ranked.sort(key=lambda x: x['Рейтинг'], reverse=True)
        # excel_output_file.output_in_cell(current_item['поиск'])
        excel_output_file.output_col_names(markets_ranked[0])
        for market in markets_ranked:
            excel_output_file.output_values(market)
        excel_output_file.auto_size_cols()
        excel_output_file.output_in_cell(current_item['поиск'])
        excel_output_file.save()
        excel_output_file.new_sheet()
        # output.write(f'{current_item["поиск"]}\n')
        # print(*markets_ranked, sep='\n', file=output)
        # output.write(f'{markets_ranked}')
        # output.write('-' * 15 + '\n')
        # print(current_item['поиск'])
        # pprint(markets_ranked)

    excel_input_file.close_file()
    # output.close()
    print(datetime.now() - time)


if __name__ == '__main__':
    main()

# google_browser.quit()
# market_shop_browser.quit()
