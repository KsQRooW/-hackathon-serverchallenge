from .parse_excel import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

ChromeOptions = webdriver.ChromeOptions()
ChromeOptions.add_argument('headless')
driver = webdriver.Chrome(ChromeDriverManager().install(), options=ChromeOptions)

path = 'source/poiskpostav_v1_test.xlsx'                 # Список товаров
params1 = {'стандарт': 'ГОСТ',                      # Параметры товаров 1 типа
           'покрытие': 'покрытие',
           'головка': 'головка',
           'рабочий вакуум': 'рабочий вакуум'
           }
params2 = {'СТАНДАРТ', 'ГОЛОВКА', 'ОБОЗНАЧЕНИЕ',    # Параметры товаров 2 типа
           'КЛАСС ПРОЧНОСТИ', 'МАТЕРИАЛ', 'ТИП'
           }

structuredData = struturizedata(importgoods(path), params1, params2)
