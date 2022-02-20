from wordle.game import *
from wordle.random_bot import RandomBotPlayer
import logging

FORMAT = '[%(asctime)s] %(levelname)s {%(filename)s:%(lineno)d} - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

player = RandomBotPlayer()

game = WordleGame(player)
game.start(num_games=10000)
