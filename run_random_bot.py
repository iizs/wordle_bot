from wordle.game import *
from wordle.random_bot import RandomBotPlayer
import logging
import datetime

FORMAT = '[%(asctime)s] %(levelname)s {%(filename)s:%(lineno)d} - %(message)s'
logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'logs/run_random_bot_{datetime.datetime.now().strftime("%Y%m%d%H%M")}.log')
    ]
)

player = RandomBotPlayer()

game = WordleGame(player, mode='simulation')
game.start(num_games=None)
