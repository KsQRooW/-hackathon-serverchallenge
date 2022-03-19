headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9 ',
    'Cookie': """HSID=AUI8CXLPgaDZ8Faj2; SSID=A0WtX5ku2uhNlB4gh; APISID=s4SU8Mi1AkCX2ljW/AVpZGXmRLo_o-Q6Nk; SAPISID=ppOx4pO-8s8KYJ-J/A88P5R6EnJ75Ta3nb; __Secure-1PAPISID=ppOx4pO-8s8KYJ-J/A88P5R6EnJ75Ta3nb; __Secure-3PAPISID=ppOx4pO-8s8KYJ-J/A88P5R6EnJ75Ta3nb; OTZ=6365597_44_44_123780_40_436260; SEARCH_SAMESITE=CgQI6JQB; S=billing-ui-v3=M4X--gf7WDR-st2Mw4WEzR8IMOJm649m:billing-ui-v3-efe=M4X--gf7WDR-st2Mw4WEzR8IMOJm649m; SID=HwiJaD2dAbOYPnXv_nN_H-wwSv1iWaPwCXjAGvDFGZDnmgU8o2EEHWARMRyeRiRk9x4dZw.; __Secure-1PSID=HwiJaD2dAbOYPnXv_nN_H-wwSv1iWaPwCXjAGvDFGZDnmgU82NjLUIZMoaT-p6_qN302QA.; __Secure-3PSID=HwiJaD2dAbOYPnXv_nN_H-wwSv1iWaPwCXjAGvDFGZDnmgU8P1RrG2tyYwLS5bB6Ba6NOw.; NID=511=nuAP-DzoL7FE4XS48JGVJ-Xksc4YDP9uQC9zZYLde6qbTIri4wlytl6UUt0jIZsQZLos-hCjzCsp9L-K1v037frrlROqbu1wNZjfPDaWwJgvj7N93-fIN4JRmnfFaQYGH5wgM3F8L3XxXi4HG_rONlfiiZjd1vVGZDNkplLjSbXoIuOjBS9gSnSlsAXz_l90Loi_ocrcN_k3zLovCHn-RIg-wlThgsUHtPxRUQQYRVBrBE4EQvxhHKioME0O2DsBlGk1Lf-lI01C; 1P_JAR=2022-03-08-19; DV=I9XuDPuTOUlYQAgxTl7ANXbQzWux9te-g7kjb7se6QAAAFDnUmPnDIwfWgAAADSuK0_N0U9ZJAAAAFgvVcgWkPXiEwAAAA; SIDCC=AJi4QfH5Kdd3L2AXKnUO1DLcVGRXQK4InU7WOnlioZfrymu6zi_wO6B_oMrhnOuF5yCCECopD6Rt; __Secure-3PSIDCC=AJi4QfGqEhygiCBWdhvPgja0897BLK9ELvbsXxOXZ8TVB6Zow9YE5agXy1YGS_3aC8cNp1GKsZE"""
}

login = 'login'
password = 'password'
proxy = 'xxx.xx.xx.xxx:xxxxx'

proxies = {
           'https': f'http://{login}:{password}@{proxy}'
}

path_excel_input = 'source/poiskpostav_v1_test.xlsx'  # Путь для входного Excel файла

path_excel_output = 'source/poiskpostav_OUTPUT.xlsx'  # Путь для выходного Excel файла

path_market_words = 'source/market_words.txt'  # Путь для словаря market_words.txt

path_org_types = 'source/org_types.txt'  # Путь для словаря с распространенными формами юр. лиц

path_webdriver = 'source/chromedriver.exe'  # Путь до драйвера для Selenium

excel_params1 = {'стандарт': 'ГОСТ',                        # Параметры товаров 1 типа
                 'покрытие': 'покрытие',
                 'головка': 'головка',
                 'рабочий вакуум': 'рабочий вакуум'
                 }

num_google_pages = 3                                        # Количество страниц в поиске гугл

excel_params2 = {'СТАНДАРТ', 'ГОЛОВКА', 'ОБОЗНАЧЕНИЕ',      # Параметры товаров 2 типа
                 'КЛАСС ПРОЧНОСТИ', 'МАТЕРИАЛ', 'ТИП'
                 }

# Запрещенные сайты:
# Создано с точки зрения оптимизации
# На этапе проверки "является ли сайт магазином?" слова с сайта будут по-очередно считываться, приводиться
# к нормальной форме и сопоставляться со словами из словаря market_words.txt до первого совпадения.
# То есть, в худшем случае, будут сопоставлены все слова с сайта со словарем.
# Так как часто при поиске товаров находятся просто сайты с ГОСТами, на которых очень много текста -
# Было решено забанить самые популярные сайты с ГОСТ архивами, чтобы не происходило такой длительной проверки.
Blacklist = {
    'docs.cntd.ru',
    'gost.ru',
    'gostinfo.ru',
    'standards.ru',
    'docplayer.com',
    'ru.djvu.online',
    'avito.ru'
}

# Параметры ранжирования поставщикови и весовые коэффициенты
supplier_sorting_params = {
    'Выручка': 0.2,
    'Прибыль': 0.03,
    'Стоимость': 0.05,
    'Уставный капитал': 0.03,
    'Госконтракты': 0.03,
    'Надежность': 0.2,
    'Тендер, отношение': 0.1,
    'Тендер, выиграл': 0.2,
    'Истец': 0.02,
    'Ответчик': 0.1,
    'Дата регистрации': 0.04
}
