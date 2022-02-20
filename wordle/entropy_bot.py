from .player import Player
import logging

logger = logging.getLogger(__name__)


class EntropyBotPlayer(Player):
    def make_guess(self, status):
        logger.info(f"\n{status}")
        return "arose"

    def win(self, status):
        logger.info(f"\n{status}")
        logger.info(f"Won in {status.num_tries()} tries!")

    def lose(self, status, answer):
        logger.info(f"\n{status}")
        logger.info(f"Lost! The answer was: {answer}")

    def __init__(self):
        super().__init__()
        self.__name__ = "EntropyBotPlayer"

