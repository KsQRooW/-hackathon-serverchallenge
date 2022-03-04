from datetime import datetime


class Logs:
    def __init__(self):
        self.path = 'source/logs.txt'
        self.__time = None
        self.status = None
        self.url = ''
        self.text = ''
        self.err = ' '

    @property
    def time(self):
        self.__time = datetime.now().strftime("%H:%M:%S")
        return self.__time

    def OK(self, text='', url=''):
        self.status = 'OK'
        self.text = text
        self.url = url
        print(self)
        self.clear()

    def INFO(self, text='', url=''):
        self.status = 'INFO'
        self.text = text
        self.url = url
        print(self)
        self.clear()

    def FAIL(self, text='', url='', err=' '):
        self.status = 'FAIL'
        self.text = text
        self.url = url
        self.err += err + ' '
        print(self)
        self.clear()

    def WARN(self, text='', url=''):
        self.status = 'WARN'
        self.text = text
        self.url = url
        print(self)
        self.clear()

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
