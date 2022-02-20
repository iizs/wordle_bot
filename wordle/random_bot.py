from .player import Player
from .dictionary import WordleDictionary, ExternalDictionary
import os
import logging

logger = logging.getLogger(__name__)


class RandomBotPlayer(Player):
    def make_guess(self, status):
        super().make_guess(status)
        logger.info(f"\n{status}")
        if self.previous_guess is not None:
            self.dictionary = self.dictionary.reduce(self.previous_guess, status.tries[-1][1])
        logger.info(f"{len(self.dictionary.dictionary)} candidates left")
        try:
            self.previous_guess = self.dictionary.random()
        except IndexError:
            pass
        logger.info(f"Trying: {self.previous_guess}")
        return self.previous_guess

    def win(self, status):
        super().win(status)
        logger.info(f"\n{status}")
        logger.info(f"Won in {status.num_tries()} tries!")

    def lose(self, status, answer):
        super().lose(status, answer)
        logger.info(f"\n{status}")
        logger.info(f"Lost! The answer was: {answer}")

    def game_over(self):
        logger.info("Game over!")
        logger.info(f"{self.name} won {self.wins} games, lost {self.losses} games.")
        if self.wins > 0:
            avg_guesses = sum(self.num_guesses_on_success) / len(self.num_guesses_on_success)
            logger.info(f"{self.name} had {avg_guesses:.2f} guesses on average.")
        else:
            logger.info(f"{self.name} had no successful guesses.")

    def restart(self):
        self.games += 1
        self.num_guesses = 0
        self.dictionary = self.init_dictionary
        self.previous_guess = None
        logger.info(f"Starting game #{self.games}")

    def __init__(self):
        super().__init__()
        self.name = "RandomBotPlayer"
        self.__name__ = "RandomBotPlayer"
        self.init_dictionary = ExternalDictionary(
            data_dir=os.path.join(os.getcwd(), 'data', 'dictionary', 'scrabble.merriam'),
            source="scrabble.merriam"
        )
        self.dictionary = self.init_dictionary
        self.previous_guess = None


