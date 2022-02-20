import logging

logger = logging.getLogger(__name__)


class Player:
    def __init__(self):
        self.name = None
        self.__name__ = "Player"
        self.games = 0
        self.wins = 0
        self.losses = 0
        self.num_guesses_on_success = []
        self.num_guesses = 0

    def set_name(self, name):
        self.name = name

    def print_status(self, status):
        print(status)

    def make_guess(self, status):
        self.num_guesses = len(status.tries) + 1

    def win(self, status):
        self.wins += 1
        self.num_guesses_on_success.append(self.num_guesses)

    def lose(self, status, answer):
        self.losses += 1

    def game_over(self):
        print("Game over!")
        print(f"{self.name} won {self.wins} games, lost {self.losses} games.")
        if self.wins > 0:
            avg_guesses = sum(self.num_guesses_on_success) / len(self.num_guesses_on_success)
            print(f"{self.name} had {avg_guesses:.2f} guesses on average.")
        else:
            print(f"{self.name} had no successful guesses.")

    def restart(self):
        self.games += 1
        self.num_guesses = 0
        print(f"Starting game #{self.games}")


class HumanPlayer(Player):
    def make_guess(self, status):
        super().make_guess(status)
        print(status)
        return input("Enter a guess: ")

    def win(self, status):
        super().win(status)
        print(status)
        print("You win!")

    def lose(self, status, answer):
        super().lose(status, answer)
        print(status)
        print("You lose! The answer was:", answer)

    def __init__(self):
        super().__init__()
        self.__name__ = "HumanPlayer"
