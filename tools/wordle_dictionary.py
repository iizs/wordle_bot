import os
import json


class WordleDictionary:
    DEFAULT_DATA_DIR = os.path.join(os.getcwd(), 'data', 'dictionary', 'scrabble.merriam')
    DEFAULT_SOURCE = 'scrabble.merriam'
    DATA_FILE_PATTERN = '{}.{}{:02d}.json'
    DEFAULT_MAX_WORD_LENGTH = 5

    ALPHABET = 'abcdefghijklmnopqrlstuvwxyz'
    MIN_WORD_LENGTH = 5

    def __init__(self, data_dir=DEFAULT_DATA_DIR, source=DEFAULT_SOURCE, max_word_length=DEFAULT_MAX_WORD_LENGTH):
        self.data_dir = data_dir
        self.source = source
        self.max_word_length = max_word_length
        self.dictionary = {}
        self.num_words = 0
        self.num_by_letter = {letter: 0 for letter in self.ALPHABET}
        self.wordset_by_letter = {letter: set() for letter in self.ALPHABET}
        self.wordset_by_letters_and_positions = {
            letter: {idx: set() for idx in range(1, 6)} for letter in self.ALPHABET
        }
        for c in WordleDictionary.ALPHABET:
            for l in range(WordleDictionary.MIN_WORD_LENGTH, self.max_word_length + 1):
                file_path = os.path.join(self.data_dir, WordleDictionary.DATA_FILE_PATTERN.format(self.source, c, l))
                try:
                    with open(file_path) as f:
                        data = json.load(f)
                        for word in data['data']:
                            self.dictionary[word] = len(word)
                            self.num_words += 1
                            for idx, ch in enumerate(word):
                                self.num_by_letter[ch] += 1
                                self.wordset_by_letter[ch].add(word)
                                self.wordset_by_letters_and_positions[ch][idx + 1].add(word)
                except FileNotFoundError:
                    continue

    def exists(self, word):
        return word in self.dictionary

    def get_num_words(self):
        return self.num_words

    def get_num_by_letter(self):
        return self.num_by_letter

    def get_words_including_letter(self, letter):
        return self.wordset_by_letter[letter]

    def get_words_by_letters(self, letters):
        words = set(self.wordset_by_letter[letters[0]])
        for l in letters[1:]:
            words = words.intersection(self.wordset_by_letter[l])
            if len(words) == 0:
                return None
        return words

    def get_words_by_letter_and_position(self, letter, position):
        return self.wordset_by_letters_and_positions[letter][position]
