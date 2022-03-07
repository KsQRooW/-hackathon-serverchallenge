# TEST GET INN

from modules.class_SpecificParsing import SpecificParsing

testData = {
    'konsulavto.ru',
    'kmzsibmash.ru',
    'molotkrep.ru',
    'metizural.ru',
    'rosspeckrepeg.ru',
    'tdm-neva.ru',
    'xn----jtbaeggiethskfo2f3c.xn--p1ai'
    'garant-metiz.ru',
    'metizural.ru',
    'rosspeckrepeg.ru',
    'tdm-neva.ru',
    'www.pulscen.ru',
    'polimer-prom.kiev.ua',
    'vysota-17.ru',
    'allbearing.ru',
    'bizorg.su',
    'ecotop-nsk.ru',
    'prom.ua',
    'rost-s.ru',
    'rti-altai.ru',
    'sibkraspolimer.ru'
}
parser = SpecificParsing()
for url in testData:
    print('   ', url)
    print('ИНН:', parser.find_inn_by_url(url))


"""
# Поиск ИНН на сайте магазина
def find_inn_from_site(site):
    googleUrl = 'https://www.google.com/search?as_q=%D0%B8%D0%BD%D0%BD&as_qdr=all&as_sitesearch=' + site + '&as_occt=any&safe=images'
    driver.get(googleUrl)
    classes_with_descr = driver.find_elements(By.CLASS_NAME, 'VwiC3b')
    markets_descr = set()
    for i in classes_with_descr:
        txtdescr = i.find_element(By.TAG_NAME, 'span').text
        i = txtdescr.find('ИНН')
        if i != -1:
            inn = txtdescr[i+4:i+14]        # Добавить различные разделители (ИНН: ххх, ИНН - ххх, ИНН   ххх и тд)
            if inn.isalnum():
                return int(inn)
    return False


# Поиск ИНН по адресу сайта
def find_inn_by_url(url):
        # https://spark-interfax.ru/search
        # https://www.kartoteka.ru/
    return 0


# Поиск ИНН по названию компании
def find_inn_by_name(name):
        # https://sbis.ru/contragents
        # https://spark-interfax.ru/search
        # https://www.audit-it.ru/contragent/
        # https://www.kartoteka.ru/
        # https://www.list-org.com/search
        # https://classinform.ru/proverka-kontragenta.html
    return 0


# Парсинг информации о компании по ИНН
def getsupplierinfo(inn, url):
    # https://sbis.ru/contragents/7725385022/773601001
    return False


# Проверка поставщиков
def checksupplier(suppliers):
    trusted_suppliers = ()
    for s in suppliers:
        log('Поиск ИНН для сайта', s['url'])
        inn = find_inn_from_site(s['url'])
        if not inn:
            log('ИНН на сайте магазина не найден')
            inn = find_inn_by_url(s['url'])
            if not inn:
                log('ИНН по адресу сайта не найден')
                inn = find_inn_by_name(s['name'])
                if not inn:
                    log('ИНН по названию не найден. Сайт', s['url'], 'исключен')
                    continue
        log('ИНН для сайта', s['url'], 'найден:', inn)
        supplierinfo = getsupplierinfo(inn, s['url'])
        if supplierinfo:
            trusted_suppliers += (supplierinfo,)
    return trusted_suppliers

"""