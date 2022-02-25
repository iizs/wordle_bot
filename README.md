# Wordle Helper

## Get Dictionary

For the game, a dictionary of words is needed. 
There could be many options, 
but the [Scrabble Dictionary from Merriam-Webster](https://scrabble.merriam.com/) 
and [Wordle](https://www.nytimes.com/games/wordle/index.html) itself have been chosen.


* ```get_scrabble_dictionary.py``` will download all the 5-letter words from the dictionary. 
* ```generate_wordle.py``` will generate a dictionary from wordle game source code. 
(Already downloaded and embedded in the code.)

Dictionary files are already downloaded in the `data` folder. 
In case of any problems, these scripts can be used to download the dictionary.

## Play Game

With `play_game.py`, you can play the Wordle game by yourself.

## Simulate Game

Make bots play the Wordle game.

Currently, there are two bots:

* ```run_random_bot.py```: Randomly picks a word from the dictionary. 
* ```run_entropy_bot.py```: Picks the word with the highest entropy. 
See the YouTube video, ["Solving Wordle using information theory"](https://youtu.be/v68zYyaEmEA) for more details.


