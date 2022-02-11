import re
from typing_extensions import Self
import unicodedata


class WordChecker:
    def __init__(self, file_path):
        with open(file_path, 'r', encoding="utf-8") as word_base_file:
            self.word_base = word_base_file.read().split('\n')
            print (f'Dictionary has {len(self.word_base)} words')

    def check_word(self, word):
        left = 0
        right = len(self.word_base) - 1
        while left <= right:
            print (f'[{left}, {right}]')
            mid = (left + right) // 2
            if self.word_base[mid] > word:
                print (f'{self.word_base[mid]} > {word}')
                right = mid - 1
            else:
                print (f'{self.word_base[mid]} <= {word}')
                left = mid + 1
        return word == self.word_base[right]

    def check_words(self, words):
        for word in words:
            print(f'Checking word {word}')
            word = word.lower()

            # if word not in self.word_base:
            #     return False

            if self.check_word(word) == False:
                print (f'This is not a valid word')
                return False
                
        return True

    def remove_accents(input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        only_ascii = nfkd_form.encode('ASCII', 'ignore')
        return only_ascii