import pygame
from Board import Board, BoardNode, DisplayBoard
from Pieces import Pieces
from Consts import Colors, MoveType, reset_params, BoardParameters
from ComputerAI import ComputerAI
from Move import Move
from GameTerminal import GameTerminal
from typing import List, Tuple
from GameObjectInterface import GameObjectInterface


class Game(GameObjectInterface):

    def __init__(self, difficult: int,
                 user_color=Colors['WHITE'],
                 computer_color=Colors['BLACK']):
        """
        This function is the default constructor of the game object.
        """
        super(Game, self).__init__()
        pygame.init()

        self.board_width = (BoardParameters['CELL_WIDTH'] *
                            BoardParameters['COLS'])

        self.board_height = (BoardParameters['CELL_HEIGHT'] *
                             BoardParameters['ROWS'])

        self.screen_width = (self.board_width +
                             BoardParameters['TERMINAL_WIDTH'])

        self.screen_height = self.board_height

        self.main_screen = pygame.display.set_mode([self.screen_width,
                                                    self.screen_height])

        pygame.display.set_caption("Chess")

        self.clock = pygame.time.Clock()

        self.quit_game_flag = False
        self.pause_game_flag = False
        self.is_user_turn = (user_color == Colors['WHITE'])

        self.user_color = user_color
        self.computer_color = computer_color

        self.computer_ai = ComputerAI(difficult,
                                      computer_color=computer_color,
                                      user_color=user_color)

        self.board = Board.default_ctor(user_color=user_color)
        self.display_board = DisplayBoard(self.main_screen, self.board)

        self.terminal = GameTerminal(self.board_width,
                                     0, BoardParameters['TERMINAL_WIDTH'],
                                     self.screen_width,
                                     self.main_screen,
                                     self)

    def handle_user_piece_selection(self):
        """
        This function handles the operation of piece selection from the user
        point of view.
        :return: returns the list of parameters [from_row, from_col, to_row,
        to_col, selected piece, all_possible moves]
        """

        from_row, from_col = self.get_cell(pygame.mouse.get_pos())
        selected_piece = self.board.get_piece_at(from_row, from_col)
        selected_piece_color = self.board.get_piece_color_at(from_row, from_col)

        # Check whether user selected is piece
        if selected_piece != Pieces.NONE and \
                selected_piece_color == self.user_color:

            self.display_board.display_selected(from_row, from_col,
                                                MoveType['SELECT'])

            # Compute all possible moves for that piece.
            all_possible_moves = \
                self.board.get_all_possible_moves(from_row, from_col)

            if all_possible_moves:
                self.display_board.display_all_possible_moves(
                    all_possible_moves)
        else:
            [from_row, from_col,
             selected_piece, all_possible_moves] = [-1, -1, Pieces.NONE, []]

        return from_row, from_col, selected_piece, all_possible_moves

    def handle_users_piece_movement(self, new_move, all_possible_moves):
        """
        This function handles the piece movement operation of the user. It does
        it from both perspectives: the first,
        is the update of the logical board; the second, is the update of the
        display.
        :param new_move: the move to be performed, a Move object.
        :param all_possible_moves: the list of all possible and legal moves that
        can be performed for some piece.
        :return: True, if and only if the move is done.
        """
        if new_move in all_possible_moves:
            if self.board.move_piece(new_move):
                self.pause_game_flag = True
                self.terminal.display_win_message()
            self.display_board.move_piece(new_move, all_possible_moves)
            return True

        # For debug purposes
        # print("Cannot perform users move. The move " +
        #       str(new_move) + " is illegal.")

        return False

    @staticmethod
    def get_cell(mouse_pos: Tuple[int]) -> List[int]:
        """
        This function translates the (x,y) mouse location of the screen into
        (row, col) coordinates on the board.
        :param mouse_pos:tuple of (x,y) that indicates the current mouse
        position.
        :return: the cell coordinates in the form of (row, col) on the board.
        """
        return [int(mouse_pos[1] / BoardNode.CELL_HEIGHT),
                int(mouse_pos[0] / BoardNode.CELL_WIDTH)]

    def is_mouse_click_on_board(self, mouse_pos: Tuple[int]) -> bool:
        """
        This function should be called when mouse click is recognized. It will
        determine whether the click is on the board or no. The main idea of that
        function is to help to separate clicks that done on the board and maybe
        somehow relevant to move piece and the game itself, with one that are
        appeared on the terminal aside.
        :param mouse_pos: tuple (x,y) indicates the position of the function.
        :return: True, if and only if the click is on the board.
        """
        return (0 <= mouse_pos[0] <= self.board_width and
                0 <= mouse_pos[1] <= self.board_height)

    def run_game(self):
        """
        This function responsible to run and mange the main logic of the game.
        :return: None
        """

        [from_row, from_col,
         selected_piece,
         all_possible_moves] = reset_params

        self.display_board.show_board()

        # While we not quit the game.
        while not self.quit_game_flag:
            # Look for events of the game.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game_flag = True

                # If mouse click was detected
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.is_user_turn and not self.pause_game_flag and \
                            self.is_mouse_click_on_board(mouse_pos):
                        mouse_buttons_pressed = pygame.mouse.get_pressed()

                        # Handle user selection of piece to move.
                        if mouse_buttons_pressed[0] == 1 and \
                                selected_piece == Pieces.NONE:
                            [from_row, from_col,
                             selected_piece, all_possible_moves] = \
                                self.handle_user_piece_selection()

                        # If user decides to un-select his piece.
                        elif mouse_buttons_pressed[2] == 1 and \
                                selected_piece != Pieces.NONE:
                            self.display_board.unselect(from_row,
                                                        from_col,
                                                        all_possible_moves)
                            [from_row, from_col,
                             selected_piece,
                             all_possible_moves] = reset_params

                        # Else user had already picked his piece and now he
                        # wants to move it. Handle the movement action.
                        elif mouse_buttons_pressed[0] == 1 and \
                                selected_piece != Pieces.NONE:
                            to_row, to_col = self.get_cell(
                                pygame.mouse.get_pos())
                            to_piece = self.board.get_piece_at(to_row, to_col)
                            new_move = Move(from_row, from_col, to_row, to_col,
                                            selected_piece, to_piece)
                            if self.handle_users_piece_movement(new_move,
                                                            all_possible_moves):

                                [from_row, from_col, selected_piece,
                                 all_possible_moves] = reset_params

                                self.terminal.add_move_to_print(new_move)
                                self.is_user_turn = not self.is_user_turn

                    # If user presses on the terminal and not on the board.
                    elif self.is_user_turn and \
                            not self.is_mouse_click_on_board(mouse_pos):
                        self.terminal.click_on_terminal(self.pause_game_flag)

            # Computers turn to play
            # The computation should be moved to another process/thread
            # so it will not block other operations
            if not self.is_user_turn and not self.pause_game_flag:
                move = self.computer_ai.computers_play(self.board)
                self.terminal.add_move_to_print(move)
                if self.board.move_piece(move):
                    self.pause_game_flag = True
                    self.terminal.display_win_message(winner='Computer')
                self.display_board.move_piece(move, [])
                self.is_user_turn = not self.is_user_turn

            self.clock.tick(30)

        pygame.quit()

    def quit_game(self) -> None:
        """
        This function responsible to quit the game.
        :return: None
        """
        self.quit_game_flag = True

    def restart_game(self) -> None:
        """
        This function responsible to restart the game.
        :return: None
        """
        print("Restart the game was pressed!")
        self.terminal.undo_all_moves()
        self.terminal.reset_terminal()
        self.board = Board.default_ctor(user_color=self.user_color)
        self.display_board = DisplayBoard(self.main_screen, self.board)
        self.display_board.show_board()
        self.pause_game_flag = False
        self.is_user_turn = (self.user_color == Colors['WHITE'])

    def undo_move(self) -> None:
        """
        This function is responsible to undo players last move. It actually
        undo's two last move - the first is of
        blacks and the second is of the player.
        :return: None
        """
        last_move_black = self.board.undo_move()
        last_move_white = self.board.undo_move()
        self.display_board.undo_move(last_move_black)
        self.display_board.undo_move(last_move_white)
        self.terminal.undo_move()
