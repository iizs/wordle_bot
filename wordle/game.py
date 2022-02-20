import logging
from abc import abstractmethod
from .dictionary import WordleDictionary

FORMAT = '[%(asctime)s] %(levelname)s {%(filename)s} - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)


class Player:
    def __init__(self):
        self.name = None
        self.__name__ = "Player"

    def set_name(self, name):
        self.name = name

    def print_status(self, status):
        print(status)

    @abstractmethod
    def make_guess(self, status):
        pass

    @abstractmethod
    def win(self, status):
        pass

    @abstractmethod
    def lose(self, status, answer):
        pass


class HumanPlayer(Player):
    def make_guess(self, status):
        print(status)
        return input("Enter a guess: ")

    def win(self, status):
        print(status)
        print("You win!")

    def lose(self, status, answer):
        print(status)
        print("You lose! The answer was:", answer)

    def __init__(self):
        super().__init__()
        self.__name__ = "HumanPlayer"


class WordleGameStatus:
    def __init__(self):
        self.__name__ = "WordleGameStatus"
        self.win = False
        self.tries = []

    def __str__(self):
        s = ''
        for guess, mark in self.tries:
            s += f'{guess} {mark}\n'
        return s

    def add(self, guess, mark):
        self.tries.append((guess, mark))
        if mark == '🟩🟩🟩🟩🟩':
            self.win = True


class WordleGame:
    def __init__(self, player):
        self.__name__ = "WorldeGame"
        self.player = player
        self.answer_dictionary = WordleDictionary(source='wordle.answer')
        self.valid_dictionary = WordleDictionary(source='wordle.valid')

    @staticmethod
    def mark(answer, guess):
        m = '⬛⬛⬛⬛⬛'
        for i in range(len(answer)):
            if answer[i] == guess[i]:
                m = m[0:i] + '🟩' + m[i+1:]
                answer = answer[0:i] + ' ' + answer[i+1:]
                guess = guess[0:i] + ' ' + guess[i+1:]
        for i in range(len(guess)):
            if guess[i] == ' ':
                continue
            for j in range(len(answer)):
                if answer[j] == guess[i]:
                    m = m[0:i] + '🟨' + m[i + 1:]
                    answer = answer[0:j] + ' ' + answer[j+1:]
        return m

    def start(self):
        # Generate a random word
        # give player a chance to guess
        # if player guesses correctly, game ends
        # if player guesses incorrectly, game continues and give the player hints
        # repeat 6 times
        # if player guesses incorrectly 6 times, game ends
        answer = self.answer_dictionary.random()
        status = WordleGameStatus()
        for i in range(6):
            valid_guess = False
            while not valid_guess:
                guess = self.player.make_guess(status)
                if self.valid_dictionary.exists(guess):
                    valid_guess = True
            mark = WordleGame.mark(answer, guess)
            status.add(guess, mark)
            if status.win:
                break

        if status.win:
            self.player.win(status)
        else:
            self.player.lose(status, answer)



