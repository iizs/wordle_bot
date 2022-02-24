from wordle.game import *
from wordle.entropy_bot import EntropyBotPlayer
import logging
import datetime

FORMAT = '[%(asctime)s] %(levelname)s {%(filename)s:%(lineno)d} - %(message)s'
logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f'logs/run_entropy_bot_{datetime.datetime.now().strftime("%Y%m%d%H%M")}.log')
    ]
)

player = EntropyBotPlayer()

game = WordleGame(player)
game.start(num_games=1)
