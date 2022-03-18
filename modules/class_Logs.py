from datetime import datetime


class Logs:
    def __init__(self):
        self.__time = None
        self.status = None
        self.url = ''
        self.text = ''
        self.err = ' '

    # Вычисление текущего времени
    @property
    def time(self):
        self.__time = datetime.now().strftime("%H:%M:%S")
        return self.__time

    # Лог событий выполненных успешно
    def OK(self, text='', url=''):
        self.status = 'OK'
        self.text = text
        self.url = url
        print(self)
        self.clear()

    # Лог информационных событий
    def INFO(self, text='', url=''):
        self.status = 'INFO'
        self.text = text
        self.url = url
        print(self)
        self.clear()

    # Лог неудачных событий
    def FAIL(self, text='', url='', err=' '):
        self.status = 'FAIL'
        self.text = text
        self.url = url
        if err != ' ':
            self.err += err + ' '
        print(self)
        self.clear()

    # Лог событий-предупреждений
    def WARN(self, text='', url='', err=' '):
        self.status = 'WARN'
        self.text = text
        self.url = url
        if err != ' ':
            self.err += err + ' '
        print(self)
        self.clear()

    # Очистка атрибутов
    def clear(self):
        self.status = None
        self.url = ''
        self.text = None
        self.err = ' '

    def __str__(self):
        return f"<{self.time}> {self.status}:" + self.err + f"{self.text} {self.url}"

    def __repr__(self):
        return f"<{self.time}> {self.status}:" + self.err + f"{self.text} {self.url}"


logger = Logs()
