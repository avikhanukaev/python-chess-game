from GameObjectInterface import GameObjectInterface


class Game:
    def quit_game(self):
        pass


def quit_game(game: GameObjectInterface)->None:
    game.quit_game()


def restart_game(game: GameObjectInterface)->None:
    game.restart_game()


def undo_move(game: GameObjectInterface)->None:
    game.undo_move()


def save_log(game: GameObjectInterface)->None:
    # todo complete the save log operation
    print("Save action")