headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9 ',
    # 'Cookie': """SID=GwiJaMnGGcjHi2d-ExwFiQV586UNn_jgQSGL3RA2ap1J_LEQhQ7jKtJKBNl5Z9xqgX9evw.; __Secure-1PSID=GwiJaMnGGcjHi2d-ExwFiQV586UNn_jgQSGL3RA2ap1J_LEQvguDhZPU8bMjJZAL96Qt4w.; __Secure-3PSID=GwiJaMnGGcjHi2d-ExwFiQV586UNn_jgQSGL3RA2ap1J_LEQxhO2nZv4EX_j4ujXqtljug.; HSID=AUI8CXLPgaDZ8Faj2; SSID=A0WtX5ku2uhNlB4gh; APISID=s4SU8Mi1AkCX2ljW/AVpZGXmRLo_o-Q6Nk; SAPISID=ppOx4pO-8s8KYJ-J/A88P5R6EnJ75Ta3nb; __Secure-1PAPISID=ppOx4pO-8s8KYJ-J/A88P5R6EnJ75Ta3nb; __Secure-3PAPISID=ppOx4pO-8s8KYJ-J/A88P5R6EnJ75Ta3nb; OTZ=6365597_44_44_123780_40_436260; SEARCH_SAMESITE=CgQI6JQB; S=billing-ui-v3=M4X--gf7WDR-st2Mw4WEzR8IMOJm649m:billing-ui-v3-efe=M4X--gf7WDR-st2Mw4WEzR8IMOJm649m; NID=511=epBaIIhMgoitXLxWt1QfCZXiyszEDnOjed8SuiWZZ4xUuAidGCocgJ2KYiWeMhfxJp3vIinoyK-XVWBiM6Bt5l6No_AOUieDhqPtuMkzWGX3fK5CE0Ch1f8BZfOhQAcj7tfr3AEt7ugzjRXxHuyLjNKHmKw1mMXydLM6B8zfhwhZljy1dm_LVOY-ejM7krizGpyBd7zNVZtcKno-PQXnzHYG0lXbdmNKAEQ_Mct-a2EegQ-usTninZsig8Kh_qy7HVSWN74xPNW2; GOOGLE_ABUSE_EXEMPTION=ID=1232d3369695cff1:TM=1646736193:C=r:IP=46.249.13.200-:S=zMoQYXi5cyZZAghcPFNi3ts; 1P_JAR=2022-03-08-11; DV=I9XuDPuTOUlogPVShWwBWS--BVSU9hchxDh5AdfYAQEAAFDnUmPnDIwfGgEAAOw7mDvytuuRRgAAAI3rylNz9FMWEQAAAIj4tWEufHk2k7wRAA; SIDCC=AJi4QfFhVtulAfoFXuXW-FU4iLCQCIVIeLidPc_SQP28VzIMf3OISGOvgrLpZUNzboaZlF0C3Yp4; __Secure-3PSIDCC=AJi4QfEOxCxH3n5WJnRRr6V2sFpVVSfg5Wh4W0DaFgJvJhTwS8X9F8ZfTxyGsm_tWPWunESBnew"""
}

login = 'exfC7g'
password = '2x9VWu'
proxy = '217.29.63.159:10667'


proxies = {
           'https': f'http://{login}:{password}@{proxy}'  # https Russia - 20ms
}

path_excel_input = 'source/poiskpostav_v1_test.xlsx'                 # Список товаров

path_excel_output = 'source/poiskpostav_OUTPUT.xlsx'

path_market_words = 'source/market_words.txt'

path_org_types = 'source/org_types.txt'

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
    'ru.djvu.online',
    'avito.ru'
}
