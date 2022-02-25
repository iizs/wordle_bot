from wordle_dictionary import WordleDictionary
import logging

FORMAT = '[%(asctime)s] %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info('Loading wordle dictionary...')
wd = WordleDictionary()

logger.info(f'# of word: {wd.get_num_words()}')
logger.info(f'# of letter: {wd.get_num_by_letter()}')

num_by_letter = wd.get_num_by_letter()
num_by_letter_sorted = {k: v for k, v in sorted(num_by_letter.items(), key=lambda item: item[1], reverse=True)}
logger.info(f'# of letter (sorted): {num_by_letter_sorted}')

logger.info(f'{wd.get_words_by_letters(["s", "e", "a", "o", "r"])}')
logger.info(f'{wd.get_words_by_letters(["l", "i", "t", "n", "u"])}')
logger.info(f'{wd.get_words_by_letters(["d", "c", "y", "p", "m"])}')

# logger.info(f'{len(wd.get_words_by_letter_and_position("a", 2))}')
for letter in "abcdefghijklmnopqrstuvwxyz":
    for idx in range(1, 6):
        logger.info(f'({letter}, {idx}): {len(wd.get_words_by_letter_and_position(letter, idx))}')

logger.info(f'{wd.get_words_by_letters(["s", "i", "l"])}')
for word in wd.get_words_by_letters(["s", "i", "l"]):
    if word[0]== 's' and word[2] == 'i' and word[3] == 'l' and word[4] == 'l':
        logger.info(f'{word}')