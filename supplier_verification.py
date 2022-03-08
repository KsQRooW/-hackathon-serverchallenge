# TEST GET INN

from modules.class_Supplier import Supplier

testData = {
    'tdm-neva.ru',
    'allbearing.ru',
    'prom.ua',
    'rost-s.ru',
    'sibkraspolimer.ru'
}
parser = Supplier()
for url in testData:
    parser.find_inn_by_url(url)
