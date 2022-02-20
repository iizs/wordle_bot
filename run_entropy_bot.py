from wordle.game import *
from wordle.entropy_bot import EntropyBotPlayer
import logging

FORMAT = '[%(asctime)s] %(levelname)s {%(filename)s} - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

player = EntropyBotPlayer()

game = WordleGame(player)
game.start()