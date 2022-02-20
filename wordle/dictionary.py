import os
import json
import random


class WordleDictionary:
    DEFAULT_DATA_DIR = os.path.join(os.getcwd(), 'data', 'dictionary', 'wordle')
    DEFAULT_SOURCE = 'wordle.answer'
    DATA_FILE_PATTERN = '{}.{}{:02d}.json'
    ALPHABET = 'abcdefghijklmnopqrlstuvwxyz'

    def __init__(self, data_dir=DEFAULT_DATA_DIR, source=DEFAULT_SOURCE):
        self.data_dir = data_dir
        self.source = source
        self.dictionary = {}
        for c in WordleDictionary.ALPHABET:
            file_path = os.path.join(self.data_dir, WordleDictionary.DATA_FILE_PATTERN.format(self.source, c, 5))
            try:
                with open(file_path) as f:
                    data = json.load(f)
                    for word in data['data']:
                        self.dictionary[word] = len(word)
            except FileNotFoundError:
                continue

    def exists(self, word):
        return word in self.dictionary

    def random(self):
        return random.choice(list(self.dictionary.keys()))