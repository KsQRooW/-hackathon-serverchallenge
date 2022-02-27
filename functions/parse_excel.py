# Импорт товаров из Excel файла
def importgoods(path):
    import openpyxl
    excel = openpyxl.open(path, read_only=True)
    sheet = excel.active
    initialData = ()
    for row in range(2, sheet.max_row):
        initialData += (sheet[row][1].value[2:],)
    excel.close()
    return initialData


# Структурирование каждой строки
def struturizedata(initialData, params1, params2):
    import re

    # Выделение параметра и значения в каждой паре
    def pars(s):
        spl = re.split(r'' + restr, s)[1:]
        return spl[0].lower(), spl[1].strip().lower()

    # Генерирует выбранный порядок параметров для поискового запроса
    def addtosearch(*params):
        search = ()
        for temp in params:
            if temp in structName:
                if temp == 'головка' or temp == 'класс прочности':
                    search += (temp, structName[temp])
                else:
                    search += (structName[temp],)
        return search

    structuredData = ()
    for rawName in initialData:
        structName = {'исходная строка': rawName}
        if rawName.find(';') == -1:                                     # Описание товара 1 типа
            restr1 = '(' + '|'.join(params1.values()) + ')'
            spl = re.split(r'' + restr1, rawName)
            if spl[1] == 'головка':
                obozn = spl[2].split()[1]
                structName['обозначение'] = obozn
                spl[2] = spl[2].replace(obozn, '')
                structName['название'] = spl[0]
            else:
                t = spl[0].split()
                structName['обозначение'] = t[-1]
                structName['название'] = ' '.join(t[:-1])
            for key, value in params1.items():
                if value in spl:
                    i = spl.index(value)
                    if key == 'стандарт':
                        structName[key] = (spl[i] + spl[i+1]).strip()
                    else:
                        structName[key] = spl[i + 1].strip()
            structName['поиск'] = structName['исходная строка']
        else:                                                           # Описание товара 2 типа
            restr = '(' + '|'.join(params2) + ')'
            name, other = rawName.split('; ')
            structName['название'] = name.lower()
            structName.update(dict(map(pars, other.split(', '))))
            addtosearch('название', 'обозначение')
            structName['поиск'] = ' '.join(addtosearch('название', 'тип', 'головка', 'обозначение', 'класс прочности', 'материал', 'стандарт'))
        structuredData += (structName,)
    return structuredData
