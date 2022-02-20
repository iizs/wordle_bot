from wordle.game import *
from wordle.player import *
import logging

FORMAT = '[%(asctime)s] %(levelname)s {%(filename)s} - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

player = HumanPlayer()

game = WordleGame(player)
game.start()
