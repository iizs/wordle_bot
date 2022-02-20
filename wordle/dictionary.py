import os
import json
import random
import logging

logger = logging.getLogger(__name__)


class WordleDictionary:
    ALPHABET = 'abcdefghijklmnopqrlstuvwxyz'

    def __init__(self):
        self.dictionary = {}

    def exists(self, word):
        return word in self.dictionary

    def random(self):
        return random.choice(list(self.dictionary.keys()))

    def reduce(self, word, mask):
        return MaskedDictionary(self, word, mask)


class ExternalDictionary(WordleDictionary):
    DEFAULT_DATA_DIR = os.path.join(os.getcwd(), 'data', 'dictionary', 'wordle')
    DEFAULT_SOURCE = 'wordle.answer'
    DATA_FILE_PATTERN = '{}.{}{:02d}.json'

    def __init__(self, data_dir=DEFAULT_DATA_DIR, source=DEFAULT_SOURCE):
        super().__init__()
        self.data_dir = data_dir
        self.source = source

        for c in WordleDictionary.ALPHABET:
            file_path = os.path.join(self.data_dir, ExternalDictionary.DATA_FILE_PATTERN.format(self.source, c, 5))
            try:
                with open(file_path) as f:
                    data = json.load(f)
                    for word in data['data']:
                        self.dictionary[word] = 1
            except FileNotFoundError:
                continue


class MaskedDictionary(WordleDictionary):
    def __init__(self, parent_dictionary, mask_word, mask):
        super().__init__()
        for word in parent_dictionary.dictionary:
            m = self.match(word, mask_word, mask)
            logger.debug(f'{mask_word} {word} {mask}-> {m}')
            if m:
                self.dictionary[word] = 1

    def match(self, word, mask_word, mask):
        for i in range(len(mask_word)):
            if mask[i] == '🟩':
                if mask_word[i] != word[i]:
                    return False
                mask_word = mask_word[0:i] + ' ' + mask_word[i+1:]
                word = word[0:i] + ' ' + word[i+1:]
                mask = mask[0:i] + ' ' + mask[i+1:]

        for i in range(len(mask_word)):
            if mask_word[i] == ' ':
                continue
            if mask[i] == '🟨':
                found = False
                for j in range(len(word)):
                    if mask_word[i] == word[j]:
                        mask_word = mask_word[0:i] + ' ' + mask_word[i + 1:]
                        word = word[0:j] + ' ' + word[j + 1:]
                        mask = mask[0:i] + ' ' + mask[i + 1:]
                        found = True
                        break
                if not found:
                    return False

        for i in range(len(mask_word)):
            if mask_word[i] == ' ':
                continue
            if mask[i] == '⬛':
                if word.__contains__(mask_word[i]):
                    return False
        return True


