from .player import Player, BotPlayer
from .dictionary import WordleDictionary, ExternalDictionary
import os
import logging

logger = logging.getLogger(__name__)


class RandomBotPlayer(BotPlayer):
    def make_guess(self, status):
        super().make_guess(status)
        logger.info(f"\n{status}")

        if self.previous_guess is not None:
            if status.last_guess_was_valid:
                self.dictionary = self.dictionary.reduce(self.previous_guess, status.tries[-1][1])
            else:
                self.dictionary.remove_word(self.previous_guess)

        logger.info(f"{len(self.dictionary.dictionary)} candidates left")
        try:
            self.previous_guess = self.dictionary.random()
        except IndexError:
            pass
        logger.info(f"Trying: {self.previous_guess}")
        return self.previous_guess

    def restart(self):
        super().restart()
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


