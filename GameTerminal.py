import pygame
from Consts import Colors, Fonts
from Pieces import Pieces
from TextHandler import TextHandler
from Button import Button
import ButtonFunctionality
from GameObjectInterface import GameObjectInterface


class GameTerminal:
    """ This class is responsible for logging the game on the side of the screen
    and for presenting user with basics 'menu' operations like start new game, 
    undo some move and so on. """

    def __init__(self, top_x: int, top_y: int, width: int, height: int,
                 dest: pygame.Surface, game: GameObjectInterface):
        """
        Default c'tor
        :param top_x: int, the x coordinate of the terminal.
        :param top_y: int, the y coordinate of the terminal.
        :param width: int, the width of the terminal screen.
        :param height: int, the height of the terminal screen.
        :param dest: pygame.Surface, the surface to blit the terminal on.
        :param game: Game, the game to perform operations on.
        """
        self.top_x = top_x
        self.top_y = top_y
        self.width = width
        self.height = height
        self.destination = dest
        self.move_stack_left = []
        self.move_stack_right = []

        self.left_moves_x_coordinate = 20
        self.right_moves_x_coordinate = 200

        self.moves_text = TextHandler(Fonts['Regular'],
                                      Colors['BLACK'], 20, self.destination)
        self.big_title = TextHandler(Fonts['Bold'],
                                     Colors['BLACK'], 30, self.destination)
        self.cols = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        self.rows = ['8', '7', '6', '5', '4', '3', '2', '1']

        self.piece_letter = {
            Pieces.WHITE_KING: 'K',
            Pieces.BLACK_KING: 'K',

            Pieces.WHITE_QUEEN: 'Q',
            Pieces.BLACK_QUEEN: 'Q',

            Pieces.WHITE_BISHOP: 'B',
            Pieces.BLACK_BISHOP: 'B',

            Pieces.WHITE_HORSE: 'N',
            Pieces.BLACK_HORSE: 'N',

            Pieces.WHITE_ROOK: 'R',
            Pieces.BLACK_ROOK: 'R',

            Pieces.WHITE_PAWN: 'P',
            Pieces.BLACK_PAWN: ' P'
        }

        self.quit_button = Button(830, 790, "Quit",
                                  ButtonFunctionality.quit_game,
                                  [game], self.destination)
        self.restart_button = Button(880, 790, "New Game",
                                     ButtonFunctionality.restart_game, [game],
                                     self.destination)
        self.undo_move_button = Button(985, 790, "Undo Move",
                                       ButtonFunctionality.undo_move,
                                       [game], self.destination)
        self.save_log_button = Button(1095, 790, "Save Log",
                                      ButtonFunctionality.save_log,
                                      [game], self.destination)

        self.display_back_ground()

    def display_back_ground(self) -> None:
        """
        This function responsible for displaying the background terminal on the
        screen.
        :return: None
        """

        pygame.draw.rect(self.destination, Colors['GRAY'],
                         [self.top_x, self.top_y,
                          self.width, self.height])

        pygame.draw.rect(self.destination, Colors['BLACK'],
                         [self.top_x + 122, self.top_y + 19, 150, 40], 2)

        pygame.draw.line(self.destination, Colors['BLACK'],
                         (103 * 8, 103 * 7 + 60),
                         (103 * 8 + self.width, 103 * 7 + 60), 1)

        self.big_title.display_message(self.top_x + 130,
                                       self.top_y + 20, "Game Log")

        self.display_menu()
        pygame.display.update()

    def print_moves(self) -> None:
        """
        This function prints the moves on the terminal screen.
        todo This function should be rewritten in more elegant way
        :return: None
        """

        for i in range(0, len(self.move_stack_left), 2):
            # Print the number of the move.
            self.moves_text.display_message(self.top_x +
                                            self.left_moves_x_coordinate,
                                            self.top_y + 60 + 10 * (i + 1),
                                            str(int(i / 2) + 1))
            # Print white move
            self.moves_text.display_message(self.top_x +
                                            self.left_moves_x_coordinate + 30,
                                            self.top_y + 60 + 10 * (i + 1),
                                            self.move_stack_left[i])
            # Print black move
            if i < len(self.move_stack_left) - 1:
                self.moves_text.display_message(self.top_x +
                                                self.left_moves_x_coordinate
                                                + 100,
                                                self.top_y + 60 + 10 * (i + 1),
                                                self.move_stack_left[i + 1])

        for i in range(0, len(self.move_stack_right), 2):
            # Print the number of the move.
            self.moves_text.display_message(self.top_x +
                                            self.right_moves_x_coordinate,
                                            self.top_y + 60 + 10 * (i + 1),
                                            str(int(i / 2) + 16))
            # Print white move
            self.moves_text.display_message(self.top_x +
                                            self.right_moves_x_coordinate + 30,
                                            self.top_y + 60 + 10 * (i + 1),
                                            self.move_stack_right[i])
            # Print black move
            if i < len(self.move_stack_right) - 1:
                self.moves_text.display_message(self.top_x +
                                                self.right_moves_x_coordinate +
                                                100,
                                                self.top_y + 60 + 10 * (i + 1),
                                                self.move_stack_right[i + 1])

    def add_move_to_print(self, move):
        """ This function responsible for logging the objects on the screen.
        :param: move, Move object that represents the move that should be logged
        """

        if len(self.move_stack_left) == 30:
            self.move_stack_right.append(self.convert_move_to_message(move))
        else:
            self.move_stack_left.append(self.convert_move_to_message(move))

        # self.print_moves()
        self.reset_terminal()

    def convert_move_to_message(self, move) -> None:
        """ This function is helper function that translates the move to message
        to be printed on the screen.
        :param move: Move, the move to be printed on the screen.
        :return: None
        """
        piece_letter = self.piece_letter[move['from_piece']]
        eating = 'x' if move['to_piece'] != Pieces.NONE else ''
        target_cell = self.cols[move['to_col']] + self.rows[move['to_row']]
        return piece_letter + eating + target_cell

    def display_menu(self) -> None:
        """
        This function responsible to show the terminal buttons on the terminal
        screen.
        :return: None
        """
        self.quit_button.display()
        self.restart_button.display()
        self.undo_move_button.display()
        self.save_log_button.display()

    def click_on_terminal(self, game_paused=False) -> None:
        """
        This function responsible to detect click on the terminal and response
        in appropriate way.
        :return: None
        """
        if not game_paused:
            if self.undo_move_button.is_pressed():
                self.undo_move_button.perform_operation()
        if self.quit_button.is_pressed():
            self.quit_button.perform_operation()
        elif self.restart_button.is_pressed():
            self.restart_button.perform_operation()
        elif self.save_log_button.is_pressed():
            self.save_log_button.perform_operation()

    def undo_move(self) -> None:
        """
        This function responsible to 'undo move' in terms of moves that were
        printed on the terminal screen.
        :return: None
        """
        if self.move_stack_right:
            self.move_stack_right = self.move_stack_right[:-2]
        else:
            self.move_stack_left = self.move_stack_left[:-2]
        self.reset_terminal()

    def reset_terminal(self) -> None:
        """
        This function responsible to reset the terminal in visual context.
        :return: None
        """
        self.display_back_ground()
        self.display_menu()
        self.print_moves()

    def undo_all_moves(self) -> None:
        """
        This function responsible to clear all the moves out of the terminal
        screen.
        :return: None
        """
        self.move_stack_left = []
        self.move_stack_right = []

    def display_win_message(self, winner = 'User'):
        msg = "Game is over! {} won the game.".format(winner)
        self.moves_text.display_message(103 * 8, 103 * 7 + 35, msg)

