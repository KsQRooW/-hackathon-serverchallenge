from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

ChromeOptions = webdriver.ChromeOptions()
ChromeOptions.add_argument('headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=ChromeOptions)


def log(*args, sep=' ', h=''):
    from datetime import datetime
    current_datetime = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    if h != '':
        h += ': '
    print(current_datetime, '\t\t', h.upper(), sep.join(map(str, args)), sep='')


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
    """
        https://spark-interfax.ru/search
        https://www.kartoteka.ru/
    """
    return 0


# Поиск ИНН по названию компании
def find_inn_by_name(name):
    """
        https://sbis.ru/contragents
        https://spark-interfax.ru/search
        https://www.audit-it.ru/contragent/
        https://www.kartoteka.ru/
        https://www.list-org.com/search
        https://classinform.ru/proverka-kontragenta.html
    """
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


test = (
    {'url': 'konsulavto.ru', 'name': ''},
    {'url': 'terracompozit.ru', 'name': 'Терракомпозит'},
    {'url': 'appnn.ru', 'name': 'Агропромподшипник'},
    {'url': 'mir-krepega.ru', 'name': 'Мир Крепежа'}
)
checksupplier(test)
driver.quit()
