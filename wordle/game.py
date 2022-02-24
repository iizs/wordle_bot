import logging
from .dictionary import ExternalDictionary
from .util import mark

logger = logging.getLogger(__name__)


class WordleGameStatus:
    def __init__(self):
        self.__name__ = "WordleGameStatus"
        self.win = False
        self.last_guess = None
        self.last_guess_was_valid = True
        self.tries = []

    def __str__(self):
        s = ''
        if not self.last_guess_was_valid:
            s += f'Invalid guess: {self.last_guess}\n'
        for guess, mark_result in self.tries:
            s += f'{guess} {mark_result}\n'
        return s

    def set_as_invalid_guess(self, guess):
        self.last_guess = guess
        self.last_guess_was_valid = False

    def add(self, guess, mark_result):
        self.tries.append((guess, mark_result))
        self.last_guess = guess
        self.last_guess_was_valid = True
        if mark_result == '🟩🟩🟩🟩🟩':
            self.win = True

    def num_tries(self):
        return len(self.tries)


class WordleGame:
    def __init__(self, player):
        self.__name__ = "WorldeGame"
        self.player = player
        self.answer_dictionary = ExternalDictionary(source='wordle.answer')
        self.valid_dictionary = ExternalDictionary(source='wordle.valid')

    def start(self, num_games=1):
        # Generate a random word
        # give player a chance to guess
        # if player guesses correctly, game ends
        # if player guesses incorrectly, game continues and give the player hints
        # repeat 6 times
        # if player guesses incorrectly 6 times, game ends
        for n in range(num_games):
            self.player.restart()
            answer = self.answer_dictionary.random()
            status = WordleGameStatus()
            for i in range(6):
                valid_guess = False
                while not valid_guess:
                    guess = self.player.make_guess(status)
                    if self.valid_dictionary.exists(guess):
                        valid_guess = True
                    status.set_as_invalid_guess(guess)
                m = mark(answer, guess)
                status.add(guess, m)
                if status.win:
                    break

            if status.win:
                self.player.win(status)
            else:
                self.player.lose(status, answer)
        self.player.game_over()
