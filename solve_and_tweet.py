import logging
import datetime
from wordle.webdriver import WordleWebDriver
from wordle.entropy_bot import EntropyBotPlayer
from wordle.player import HumanPlayer

FORMAT = '[%(asctime)s] %(levelname)s {%(filename)s:%(lineno)d} - %(message)s'
logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            f'logs/run_random_bot_{datetime.datetime.now().strftime("%Y%m%d%H%M")}.log',
            encoding='UTF-8',
        )
    ]
)

logger = logging.getLogger(__name__)

player = EntropyBotPlayer()
# player = HumanPlayer()
wordle_web_driver = WordleWebDriver(player)
is_solved = wordle_web_driver.start_game()
if is_solved:
    logger.info("Success")
else:
    logger.info("Failed")

wordle_web_driver.get_share_texts()

input("type anything to continue")
