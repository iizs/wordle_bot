from abc import abstractmethod


class Player:
    def __init__(self):
        self.name = None
        self.__name__ = "Player"

    def set_name(self, name):
        self.name = name

    def print_status(self, status):
        print(status)

    @abstractmethod
    def make_guess(self, status):
        pass

    @abstractmethod
    def win(self, status):
        pass

    @abstractmethod
    def lose(self, status, answer):
        pass


class HumanPlayer(Player):
    def make_guess(self, status):
        print(status)
        return input("Enter a guess: ")

    def win(self, status):
        print(status)
        print("You win!")

    def lose(self, status, answer):
        print(status)
        print("You lose! The answer was:", answer)

    def __init__(self):
        super().__init__()
        self.__name__ = "HumanPlayer"
