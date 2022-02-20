from wordle.game import *
from wordle.player import *

player = HumanPlayer()

game = WordleGame(player)
game.start()
