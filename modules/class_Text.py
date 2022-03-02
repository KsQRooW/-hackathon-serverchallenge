from string import punctuation
from pymorphy3 import MorphAnalyzer

stop_extensions = r'(\.pdf\Z)|(\.xls\Z)|(\.xlsx\Z)|(\.swf\Z)|(\.ps\Z)|(\.dwf\Z)|(\.kml\Z)|' \
                  r'(\.kmz\Z)|(\.gpx\Z)|(\.hwp\Z)|(\.ppt\Z)|(\.pptx\Z)|(\.doc\Z)|(\.docx\Z)|' \
                  r'(\.odp\Z)|(\.ods\Z)|(\.odt\Z)|(\.rtf\Z)|(\.svg\Z)|(\.tex\Z)|(\.txt\Z)|' \
                  r'(\.text \Z)|(\.wml\Z)|(\.wap\Z)|(\.xml\Z)'


class Text:
    def __init__(self, word: str | set = ''):
        self.__word = word
        self.analyzer = MorphAnalyzer()

    @property
    def word(self):
        return self.__word

    @word.setter
    def word(self, word: str | set):
        if not isinstance(word, (set, str)):
            raise TypeError(f"Передан класс {type(word)}. Ожидался класс str или set.")
        self.__word = word

    def clean(self):
        self.word = ''

    @staticmethod
    def punct_remover(word: str, set_punctuation):
        intersection = set_punctuation.intersection(word)
        for symbol in intersection:
            word = word.replace(symbol, '')
        return word

    # Удаление пунктуации в слове/множестве
    def remove_punctuation(self):
        set_punctuation = set(punctuation)
        if isinstance(self.word, str):
            result = self.punct_remover(self.word, set_punctuation)
            self.word = result
        elif isinstance(self.word, set):
            result = set()
            for one_word in self.word:
                result.add(self.punct_remover(one_word, set_punctuation))
            self.word = result

    # Приведение слова к нормальной форме (лемматизация)
    def normal_form(self):
        if isinstance(self.word, str):
            self.word = self.analyzer.normal_forms(self.word)[0]
        elif isinstance(self.word, set):
            result = set()
            for one_word in self.word:
                result.add(self.analyzer.normal_forms(one_word)[0])
            self.word = result

    # Проверка: присутствует ли хоть одно слово из text в множестве set_
    @staticmethod
    def word_matches(text, set_):
        check = False
        words_cleaner = Text()
        for word in text.split():
            words_cleaner.word = word
            words_cleaner.remove_punctuation()
            words_cleaner.normal_form()
            if words_cleaner.word in set_:
                check = True
                break
            words_cleaner.clean()
        return check

    # Создание множества market_words
    def read_file(self, file_name: str):
        self.word = set()
        with open(file_name, encoding='utf-8') as file:
            for line in file:
                self.word.add(line.lower().strip())

