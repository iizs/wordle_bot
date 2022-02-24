import os
import json
import random
import math
import logging
from .util import match, mark

logger = logging.getLogger(__name__)


class WordleDictionary:
    ALPHABET = 'abcdefghijklmnopqrlstuvwxyz'

    def __init__(self):
        self.dictionary = {}

    def exists(self, word):
        return word in self.dictionary

    def random(self):
        return random.choice(list(self.dictionary.keys()))

    def reduce(self, mask_word, mask):
        return MaskedDictionary(self, mask_word, mask)

    def remove_word(self, word):
        if word in self.dictionary:
            del self.dictionary[word]


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
            m = match(word, mask_word, mask)
            logger.debug(f'{mask_word} {word} {mask}-> {m}')
            if m:
                self.dictionary[word] = 1


class EntropyDictionary(ExternalDictionary):

    def __init__(self, data_dir=ExternalDictionary.DEFAULT_DATA_DIR, source=ExternalDictionary.DEFAULT_SOURCE):
        super().__init__(data_dir, source)
        self.candidates = list(self.dictionary.keys())
        self.calculate_entropy()
        self.initial_entropy = self.dictionary.copy()

    def reset(self):
        self.candidates = list(self.dictionary.keys())
        self.dictionary = self.initial_entropy.copy()

    def reduce(self, mask_word, mask):
        for word in self.candidates:
            m = match(word, mask_word, mask)
            logger.debug(f'{mask_word} {word} {mask}-> {m}')
            if not m:
                self.candidates.remove(word)

    def remove_word(self, word):
        if word in self.candidates:
            self.candidates.remove(word)

    def calculate_entropy(self):
        logger.info(f'Calculating entropies for {len(self.candidates)} words')
        for word in self.dictionary:
            p = {}
            for candidate in self.candidates:
                m = mark(candidate, word)
                try:
                    p[m] += 1
                except KeyError:
                    p[m] = 1
            entropy = 0
            for m in p:
                p_m = p[m] / len(self.candidates)
                entropy += p_m * math.log2(p_m)
            entropy = -entropy
            self.dictionary[word] = entropy
        logger.info(f'Calculating entropy complete')

    def get_one(self):
        max_entropy = 0
        word = None
        for w in self.dictionary:
            if self.dictionary[w] > max_entropy:
                max_entropy = self.dictionary[w]
                word = w
        logger.info(f'{word}: {max_entropy}')
        return word
