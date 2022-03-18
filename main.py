from modules import excel_input_line_number, excel_input_file, excel_params1, excel_params2, excel_output_file  # Excel
from modules import market_shop_browser, market_words                                           # Shop
from modules import google_browser, num_google_pages                                            # Google
from modules import supplier_browser                                                            # Supplier
from pprint import pprint
from datetime import datetime


def main():
    time = datetime.now()
    for i in range(excel_input_line_number):
        # Чтение одной строки из эксель файла
        current_item = excel_input_file.readline().structurizedata(excel_params1, excel_params2)
        print(f"----- {current_item['поиск']} -----")
        markets_ranked = []
        # Три страницы поисковой выдачи
        for number in range(num_google_pages):
            google_browser.start_page = number
            google_browser.google_search(current_item['поиск'])
            # Получить список ссылок на текущей странице гугл
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
                                # Поиск ИНН по адресу сайта
                                if not supplier_browser.find_inn_by_url(market_shop_browser.domain):
                                    continue
                            # Парсинг информации по поставщику
                            if supplier_browser.parse_supplier_data():
                                # pprint(supplier_browser.supplier_data)
                                # Присвоения ранга магазину
                                supplier_browser.ranking()
                                markets_ranked.append(supplier_browser.supplier_data)

        markets_ranked.sort(key=lambda x: float(x['Рейтинг']), reverse=True)
        excel_output_file.output_col_names(markets_ranked[0])
        for market in markets_ranked:
            excel_output_file.output_values(market)
        excel_output_file.auto_size_cols()
        excel_output_file.output_in_cell(current_item['поиск'])
        excel_output_file.save()
        excel_output_file.new_sheet()

    excel_input_file.close_file()
    print(datetime.now() - time)


if __name__ == '__main__':
    main()

# google_browser.quit()
# market_shop_browser.quit()
