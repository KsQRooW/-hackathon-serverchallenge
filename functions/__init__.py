from .parse_excel import *

path = 'source/poiskpostav_v1.xlsx'                 # Список товаров
params1 = {'стандарт': 'ГОСТ',                      # Параметры товаров 1 типа
           'покрытие': 'покрытие',
           'головка': 'головка',
           'рабочий вакуум': 'рабочий вакуум'
           }
params2 = {'СТАНДАРТ', 'ГОЛОВКА', 'ОБОЗНАЧЕНИЕ',    # Параметры товаров 2 типа
           'КЛАСС ПРОЧНОСТИ', 'МАТЕРИАЛ', 'ТИП'
           }
structuredData = struturizedata(importgoods(path), params1, params2)
