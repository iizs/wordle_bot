from .player import Player, BotPlayer
from .dictionary import EntropyDictionary
import os
import logging

logger = logging.getLogger(__name__)


class EntropyBotPlayer(BotPlayer):
    def make_guess(self, status):
        super().make_guess(status)
        logger.info(f"\n{status}")

        if self.previous_guess is not None:
            if status.last_guess_was_valid:
                self.dictionary.reduce(self.previous_guess, status.tries[-1][1])
            else:
                self.dictionary.remove_word(self.previous_guess)

        logger.info(f"{len(self.dictionary.candidates)} candidates left")
        if len(status.tries) > 0:
            self.dictionary.calculate_entropy()
        try:
            self.previous_guess = self.dictionary.get_one()
        except IndexError:
            pass
        logger.info(f"Trying: {self.previous_guess}")
        return self.previous_guess

    def restart(self):
        super().restart()
        self.dictionary.reset()
        self.previous_guess = None
        logger.info(f"Starting game #{self.games}")

    def __init__(self):
        super().__init__()
        self.name = "EntropyBotPlayer"
        self.__name__ = "EntropyBotPlayer"
        self.dictionary = EntropyDictionary(
            data_dir=os.path.join(os.getcwd(), 'data', 'dictionary', 'scrabble.merriam'),
            source="scrabble.merriam"
        )
        self.previous_guess = None
