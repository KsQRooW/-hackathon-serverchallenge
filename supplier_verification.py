# TEST GET INN

from modules.class_SpecificParsing import SpecificParsing

testData = {
    'tdm-neva.ru',
    'allbearing.ru',
    'prom.ua',
    'rost-s.ru',
    'sibkraspolimer.ru'
}
parser = SpecificParsing()
for url in testData:
    parser.find_inn_by_url(url)
