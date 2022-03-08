import openpyxl
import re


class Excel:
    def __init__(self, path=None, read_only=True):
        self.initialData = ()
        self.structuredData = ()
        self.path = path
        if path:
            self.file = openpyxl.open(path, read_only=read_only)
        self.line_number = 2

    @property
    def num_goods(self):
        return self.file.active.max_row - 2

    def readline(self):
        self.initialData += (self.file.active[self.line_number][1].value[2:],)
        self.line_number += 1
        return self

    # def importgoods(self):
    #     sheet = self.file.active
    #     self.initialData = ()
    #     for row in range(2, sheet.max_row):
    #         self.initialData += (sheet[row][1].value[2:],)

    def close_file(self):
        self.file.close()

    def structurizedata(self, params1, params2):
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

        rawName = self.initialData[self.line_number-3]

        structName = {'исходная строка': rawName}
        if rawName.find(';') == -1:  # Описание товара 1 типа
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
                        structName[key] = (spl[i] + spl[i + 1]).strip()
                    else:
                        structName[key] = spl[i + 1].strip()
            structName['поиск'] = structName['исходная строка']
        else:  # Описание товара 2 типа
            restr = '(' + '|'.join(params2) + ')'
            name, other = rawName.split('; ')
            structName['название'] = name.lower()
            structName.update(dict(map(pars, other.split(', '))))
            addtosearch('название', 'обозначение')
            structName['поиск'] = ' '.join(
                addtosearch('название', 'тип', 'головка', 'обозначение', 'класс прочности', 'материал', 'стандарт')
            )
        p = {}
        for key, value in structName.items():
            if key != 'исходная строка' and key != 'поиск':
                p[key] = value
        outDict = {
            'исходная строка': structName['исходная строка'],
            'поиск': structName['поиск'],
            'параметры': p
        }
        self.structuredData += (outDict,)

        return self.structuredData[self.line_number-3]

    def output_info(self, number):
        # wb = openpyxl.open('testfile.xlsx')  # Открываем тестовый Excel файл
        self.file.create_sheet(f'Sheet{number}')  # Создаем лист с названием "Sheet1"
        worksheet = self.file[f'Sheet{number}']  # Делаем его активным
        worksheet['B4'] = 'We are writing to B4'  # В указанную ячейку на активном листе пишем все, что в кавычках
        self.file.save('testdel.xlsx')  # Сохраняем измененный файл
