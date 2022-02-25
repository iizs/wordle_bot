import os
import json
import random
import math
import logging
import heapq
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

    def len(self):
        return len(self.dictionary)


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


class SimulationDictionary(ExternalDictionary):
    def __init__(self, data_dir=ExternalDictionary.DEFAULT_DATA_DIR, source=ExternalDictionary.DEFAULT_SOURCE):
        super().__init__(data_dir=data_dir, source=source)
        self.answers = list(self.dictionary.keys())
        random.shuffle(self.answers)
        self.last_answer_idx = -1

    def random(self):
        self.last_answer_idx = (self.last_answer_idx + 1) % len(self.answers)
        return self.answers[self.last_answer_idx]


class EntropyDictionary(ExternalDictionary):

    def __init__(self, data_dir=ExternalDictionary.DEFAULT_DATA_DIR, source=ExternalDictionary.DEFAULT_SOURCE):
        super().__init__(data_dir, source)
        self.candidates = list(self.dictionary.keys())
        self.entropy_words_heap = []
        logger.info(f'Begin initial entropy calculation')
        self.calculate_entropy()
        logger.info(f'End initial entropy calculation')

        # Variables for faster entropy calculation
        self.initial_entropy_words_heap = self.entropy_words_heap.copy()
        self.top_entropy_word = heapq.nlargest(1, self.entropy_words_heap)[0][1]
        self.second_try_candidates = {}
        self.second_try_entropy_words_heap = {}

    def reset(self):
        self.candidates = list(self.dictionary.keys())
        self.entropy_words_heap = self.initial_entropy_words_heap.copy()

    def reduce(self, mask_word, mask):
        update_second_try = False
        if mask_word == self.top_entropy_word:
            if mask in self.second_try_candidates:
                self.candidates = self.second_try_candidates[mask]
                self.entropy_words_heap = self.second_try_entropy_words_heap[mask]
                logger.info(f"{len(self.candidates)} candidates left")
                logger.info(f'Calculating entropies for {len(self.candidates)} words (cached)')
                return
            else:
                update_second_try = True

        new_candidates = []
        for word in self.candidates:
            m = match(word, mask_word, mask)
            logger.debug(f'{mask_word} {word} {mask}-> {m}')
            if m:
                new_candidates.append(word)
        self.candidates = new_candidates
        logger.info(f"{len(self.candidates)} candidates left")
        self.calculate_entropy()

        if update_second_try:
            logger.info(f'Updating entropies for {mask_word} / {mask}')
            self.second_try_candidates[mask] = self.candidates
            self.second_try_entropy_words_heap[mask] = self.entropy_words_heap.copy()

    def remove_word(self, word):
        if word in self.candidates:
            self.candidates.remove(word)
        logger.info(f"{len(self.candidates)} candidates left")
        self.calculate_entropy()

    def calculate_entropy(self):
        logger.info(f'Calculating entropies for {len(self.candidates)} words')
        self.entropy_words_heap = []
        for word in self.candidates:
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
            self.entropy_words_heap.append((entropy, word))
        heapq.heapify(self.entropy_words_heap)
        logger.info(f'Calculating entropy complete')

    def get_one(self):
        top_n = heapq.nlargest(10, self.entropy_words_heap)
        for pair in top_n:
            logger.info(f'{pair[1]}: {pair[0]}')
        return top_n[0][1]
