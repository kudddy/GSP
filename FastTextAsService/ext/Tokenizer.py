from pymystem3 import Mystem
import re
from colorama import Fore, Style


class Tokenizer:
    def __init__(self):
        self.space_pattern = re.compile(r'[^.А-ЯA-ZЁ]+', re.I)

        self.m = Mystem()

        try:
            with open('nw_model/stopwords.txt') as f:
                self.stop_words = set(f.read().split('\n')) | {''}
        except FileNotFoundError:
            self.stop_words = set()
            print(f'{Fore.RED}WARNING!!! Stop-words file not found!{Style.RESET_ALL}')

    def tokenize_line(self, line):
        """
        Токенизирует одну строку
        :param line:
        :return: набор лексем (pymysteam)
        """
        try:
            return [word for word in self.m.lemmatize(
                self.space_pattern.sub(' ', line.lower())) if word.strip() not in self.stop_words]
        except BrokenPipeError:
            self.m = Mystem()
            return self.tokenize_line(line)

    def join(self, lst):
        return self.space_pattern.sub(' ', ' '.join(lst))
