from Consts import Colors
from Game import Game
from Consts import Difficulties


def main():
    game = Game(Difficulties['EASY'], Colors['WHITE'], Colors['BLACK'])
    game.run_game()


if __name__ == '__main__':
    main()
    quit()
