from wordle.dictionary import EntropyDictionary
import logging
import datetime
import os

FORMAT = '[%(asctime)s] %(levelname)s {%(filename)s:%(lineno)d} - %(message)s'
logging.basicConfig(
    format=FORMAT,
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(
            f'logs/calculate_entropy_{datetime.datetime.now().strftime("%Y%m%d%H%M")}.log',
            encoding='UTF-8',
        )
    ]
)

dictionary = EntropyDictionary(
            data_dir=os.path.join(os.getcwd(), 'data', 'dictionary', 'scrabble.merriam'),
            source="scrabble.merriam"
        )

dictionary.save_initial_entropy()
