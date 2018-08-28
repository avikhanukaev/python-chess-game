import pygame
from Pieces import Pieces
from Consts import Colors, MoveType, BoardParameters
from Move import Move
from typing import List, Tuple


class BoardNode:
    """
    This class describes each and every cell inside the logical board. Each such
    cell has two main parameters that defines it. The first one is the color of
    the cell and the second is the piece that placed inside at.
    """

    CELL_WIDTH = 103  # The size of the cell
    CELL_HEIGHT = 103

    def __init__(self, piece, cell_color):
        self.piece = piece
        self.cell_color = cell_color

    def get_color(self):
        """
        This function returns the color of the cell.
        :return: color of the cell.
        """
        return self.cell_color

    def get_piece(self):
        """
        This function returns the piece inside the cell.
        :return: piece that is inside the cell.
        """
        return self.piece

    def set_piece(self, new_piece):
        """
        This function sets new piece.
        :param: new_piece, is the piece that should be placed in cell. 
        """
        self.piece = new_piece

    def draw_cell(self):
        """
        This function resets the cell by setting the piece in it to 'None'.
        """
        self.set_piece(Pieces.NONE)


class Board:
    """ This class is controller of the board. It will be responsible for 
    all logical (not visual, but logical!) operations that we can perform 
    on the board. """

    def __init__(self):
        """ This function init the board """

        # The actual board will be list of list (matrix) of BoardNode objects. 
        self.board_mat = []

        # The colors of the players. 
        self.user_color = None
        self.computer_color = None

        # Move stack can be used to undo some move or to log the game. 
        self.move_stack = []

        # Total material. This will be used for evaluation functions. 
        self.total_material = {
            Pieces.WHITE_KING: 1,
            Pieces.WHITE_QUEEN: 1,
            Pieces.WHITE_BISHOP: 2,
            Pieces.WHITE_HORSE: 2,
            Pieces.WHITE_ROOK: 2,
            Pieces.WHITE_PAWN: 8,
            Pieces.BLACK_KING: 1,
            Pieces.BLACK_QUEEN: 1,
            Pieces.BLACK_BISHOP: 2,
            Pieces.BLACK_HORSE: 2,
            Pieces.BLACK_ROOK: 2,
            Pieces.BLACK_PAWN: 8
        }

    @staticmethod
    def default_ctor(user_color=Colors['WHITE'],
                     computer_color=Colors['BLACK']):
        """ This function is default constructor of the board. """

        board = Board()
        board.user_color = user_color
        board.computer_color = computer_color

        for i in range(0, BoardParameters['ROWS']):
            row = []
            for j in range(0, BoardParameters['COLS']):
                if i % 2 == 0:
                    if j % 2 == 0:
                        row.append(BoardNode(Pieces.NONE,
                                             Colors['CORNSILK']))
                    else:
                        row.append(BoardNode(Pieces.NONE,
                                             Colors['SADDLEBROWN']))
                else:
                    if j % 2 == 0:
                        row.append(BoardNode(Pieces.NONE,
                                             Colors['SADDLEBROWN']))
                    else:
                        row.append(BoardNode(Pieces.NONE,
                                             Colors['CORNSILK']))
            board.board_mat.append(row)

        board.set_piece_at(0, 0, Pieces.BLACK_ROOK)
        board.set_piece_at(0, 1, Pieces.BLACK_HORSE)
        board.set_piece_at(0, 2, Pieces.BLACK_BISHOP)
        board.set_piece_at(0, 3, Pieces.BLACK_QUEEN)
        board.set_piece_at(0, 4, Pieces.BLACK_KING)
        board.set_piece_at(0, 5, Pieces.BLACK_BISHOP)
        board.set_piece_at(0, 6, Pieces.BLACK_HORSE)
        board.set_piece_at(0, 7, Pieces.BLACK_ROOK)

        board.set_piece_at(7, 0, Pieces.WHITE_ROOK)
        board.set_piece_at(7, 1, Pieces.WHITE_HORSE)
        board.set_piece_at(7, 2, Pieces.WHITE_BISHOP)
        board.set_piece_at(7, 3, Pieces.WHITE_QUEEN)
        board.set_piece_at(7, 4, Pieces.WHITE_KING)
        board.set_piece_at(7, 5, Pieces.WHITE_BISHOP)
        board.set_piece_at(7, 6, Pieces.WHITE_HORSE)
        board.set_piece_at(7, 7, Pieces.WHITE_ROOK)

        for col in range(0, BoardParameters['COLS']):
            board.set_piece_at(6, col, Pieces.WHITE_PAWN)
            board.set_piece_at(1, col, Pieces.BLACK_PAWN)

        return board

    def set_piece_at(self, row, col, piece):
        """ This function sets piece on (row, col) cell on board. 
        :param: row, the row coordinate of the piece. 
        :param: col, the col coordinate of the piece. 
        :return: None """
        self.board_mat[row][col].set_piece(piece)

    def get_piece_at(self, row, col):
        """ This function returns the piece at cell with coordinates of
        (row, col).
        :param: row, the row coordinate of the piece.
        :param: col, the col coordinate of the piece.
        :return: None """
        return self.board_mat[row][col].get_piece()

    def get_cell_color_at(self, row, col):
        """ This function returns the color of cell on row x col.
        :param: row, is the row of the cell.
        :param: col, is the col of the cell.
        :return: The color of the cell."""
        return self.board_mat[row][col].get_color()

    def get_piece_color_at(self, row, col):
        """ 
        This function returns piece color on coordinates row x col. If there is
        no piece, then the function returns the color of cell.
        :param: row, is the row of the cell. 
        :param: col, is the col of the cell. 
        :return: The color of the piece, if there is one. If no, the color of
        the cell.
        """
        piece = self.get_piece_at(row, col)
        if piece == Pieces.NONE:
            return self.get_cell_color_at(row, col)
        return Pieces.get_piece_color(piece)

    def __get_list_of_moves_helper(self,
                                   from_row: int,
                                   from_col: int,
                                   list_of_possible_moves:
                                   List[Tuple[int, int]]) -> List[Move]:
        """
        Helper function. It takes initial coordinates and list of target 
        coordinates and constructs list of Move objects
        :param from_row: int, initial row coordinate
        :param from_col: int, initial col coordinate
        :param list_of_possible_moves:  List[Tuple[int,int]], list of all target 
        coordinates.
        :return: List[Move], list of moves object.
        """
        moves = []
        for m in list_of_possible_moves:
            from_piece = self.get_piece_at(from_row, from_col)
            to_piece = self.get_piece_at(m[0], m[1])
            moves.append(Move(from_row, from_col, m[0], m[1],
                              from_piece, to_piece))
        return moves

    def __all_possible_moves_pawn(self,
                                  row: int,
                                  col: int,
                                  opposite_color) -> List[Move]:
        """
        This function computes all possible and legal moves for pawn that placed
        on coordinates (row, col)
        :param row: int, row where pawn is placed.
        :param col: int, col where pawn is placed.
        :param opposite_color: the color of the opposite opponent
        :return: List[Move], the list of all possible and legal moves for that
        pawn.
        """
        moves = []
        pawn_color = self.get_piece_color_at(row, col)
        if pawn_color == Colors['WHITE']:
            if row - 1 >= 0:
                if self.board_mat[row - 1][col].get_piece() == Pieces.NONE:
                    moves.append((row - 1, col))
                if col - 1 >= 0:
                    piece_color = self.get_piece_color_at(row - 1, col - 1)
                    if piece_color == opposite_color:
                        moves.append((row - 1, col - 1))
                if col + 1 < 8:
                    piece_color = self.get_piece_color_at(row - 1, col + 1)
                    if piece_color == opposite_color:
                        moves.append((row - 1, col + 1))
            if row == 6:
                if self.board_mat[row - 2][col].get_piece() == Pieces.NONE and \
                        self.board_mat[row - 1][col].get_piece() == Pieces.NONE:
                    moves.append((row - 2, col))
        else:
            if row + 1 < 8:
                if self.board_mat[row + 1][col].get_piece() == Pieces.NONE:
                    moves.append((row + 1, col))
                if col - 1 >= 0:
                    piece_color = self.get_piece_color_at(row + 1, col - 1)
                    if piece_color == opposite_color:
                        moves.append((row + 1, col - 1))
                if col + 1 < 8:
                    piece_color = self.get_piece_color_at(row + 1, col + 1)
                    if piece_color == opposite_color:
                        moves.append((row + 1, col + 1))
            if row == 1:
                if self.board_mat[row + 2][col].get_piece() == Pieces.NONE and \
                        self.board_mat[row + 1][col].get_piece() == Pieces.NONE:
                    moves.append((row + 2, col))

        return self.__get_list_of_moves_helper(row, col, moves)

    def __is_legal_move(self, row: int, col: int, opposite_color) -> List[bool]:
        """
        This helper function responsible to decide whether the move to cell
        (row, col) on board is legal move.
        :param row: int, the destination row.
        :param col: int, the destination col.
        :param opposite_color: color, the opponents color.
        :return: List[bool, bool].
        """
        if 0 <= row <= 7 and 0 <= col <= 7:
            if self.get_piece_at(row, col) == Pieces.NONE:
                return [True, False]
            if self.get_piece_color_at(row, col) == opposite_color:
                return [True, True]
        return [False, True]

    def __all_possible_moves_bishop(self, row: int,
                                    col: int, opposite_color) -> List[Move]:
        """
        This function computes all possible and legal moves for bishop that is
        currently in cell with (row, col).
        :param row: int, the current row of the bishop.
        :param col: int, the current col of the bishop.
        :param opposite_color: color, the opponents color.
        :return: List[Move], list of all possible and legal moves of bishop.
        """
        moves = []
        temp_row, temp_col, stop = row + 1, col + 1, False
        while temp_row < 8 and temp_col < 8 and not stop:
            is_legal_move, stop = self.__is_legal_move(temp_row, temp_col,
                                                       opposite_color)
            if is_legal_move:
                moves.append((temp_row, temp_col))
            temp_row += 1
            temp_col += 1

        temp_row, temp_col, stop = row - 1, col - 1, False
        while temp_row >= 0 and temp_col >= 0 and not stop:
            is_legal_move, stop = self.__is_legal_move(temp_row, temp_col,
                                                       opposite_color)
            if is_legal_move:
                moves.append((temp_row, temp_col))
            temp_row -= 1
            temp_col -= 1

        temp_row, temp_col, stop = row - 1, col + 1, False
        while temp_row >= 0 and temp_col < 8 and not stop:
            is_legal_move, stop = self.__is_legal_move(temp_row, temp_col,
                                                       opposite_color)
            if is_legal_move:
                moves.append((temp_row, temp_col))
            temp_row -= 1
            temp_col += 1

        temp_row, temp_col, stop = row + 1, col - 1, False
        while temp_row < 8 and temp_col >= 0 and not stop:
            is_legal_move, stop = self.__is_legal_move(temp_row, temp_col,
                                                       opposite_color)
            if is_legal_move:
                moves.append((temp_row, temp_col))
            temp_row += 1
            temp_col -= 1

        return self.__get_list_of_moves_helper(row, col, moves)

    def __all_possible_moves_rook(self, row: int,
                                  col: int, opposite_color) -> List[Move]:
        """
        This function computes all possible and legal moves for rook that is
        currently in cell with (row, col).
        :param row: int, the current row of the rook.
        :param col: int, the current col of the rook.
        :param opposite_color: color, the opponents color.
        :return: List[Move], list of all possible and legal moves for rook.
        """
        moves = []
        temp_row, temp_col, stop = row + 1, col, False
        while temp_row < 8 and not stop:
            is_legal_move, stop = self.__is_legal_move(temp_row, temp_col,
                                                       opposite_color)
            if is_legal_move:
                moves.append((temp_row, temp_col))
            temp_row += 1

        temp_row, temp_col, stop = row - 1, col, False
        while temp_row >= 0 and not stop:
            is_legal_move, stop = self.__is_legal_move(temp_row, temp_col,
                                                       opposite_color)
            if is_legal_move:
                moves.append((temp_row, temp_col))
            temp_row -= 1

        temp_row, temp_col, stop = row, col + 1, False
        while temp_col < 8 and not stop:
            is_legal_move, stop = self.__is_legal_move(temp_row, temp_col,
                                                       opposite_color)
            if is_legal_move:
                moves.append((temp_row, temp_col))
            temp_col += 1

        temp_row, temp_col, stop = row, col - 1, False
        while temp_col >= 0 and not stop:
            is_legal_move, stop = self.__is_legal_move(temp_row, temp_col,
                                                       opposite_color)
            if is_legal_move:
                moves.append((temp_row, temp_col))
            temp_col -= 1

        return self.__get_list_of_moves_helper(row, col, moves)

    def __all_possible_moves_horse(self, row: int,
                                   col: int, opposite_color) -> List[Move]:
        """
        This function computes all possible and legal moves for horse that is
        currently in cell with (row, col).
        :param row: int, the current row of the horse.
        :param col: int, the current col of the horse.
        :param opposite_color: color, the opponents color.
        :return: List[Move], list of all possible and legal moves for knight.
        """
        moves = []

        if row - 2 >= 0:
            if col - 1 >= 0:
                is_legal_move = self.__is_legal_move(row - 2, col - 1,
                                                     opposite_color)[0]
                if is_legal_move:
                    moves.append((row - 2, col - 1))
            if col + 1 < 8:
                is_legal_move = self.__is_legal_move(row - 2, col + 1,
                                                     opposite_color)[0]
                if is_legal_move:
                    moves.append((row - 2, col + 1))

        if row + 2 < 8:
            if col - 1 >= 0:
                is_legal_move = self.__is_legal_move(row + 2, col - 1,
                                                     opposite_color)[0]
                if is_legal_move:
                    moves.append((row + 2, col - 1))
            if col + 1 < 8:
                is_legal_move = self.__is_legal_move(row + 2, col + 1,
                                                     opposite_color)[0]
                if is_legal_move:
                    moves.append((row + 2, col + 1))

        if col - 2 >= 0:
            if row - 1 >= 0:
                is_legal_move = self.__is_legal_move(row - 1, col - 2,
                                                     opposite_color)[0]
                if is_legal_move:
                    moves.append((row - 1, col - 2))
            if row + 1 < 8:
                is_legal_move = self.__is_legal_move(row + 1, col - 2,
                                                     opposite_color)[0]
                if is_legal_move:
                    moves.append((row + 1, col - 2))

        if col + 2 < 8:
            if row - 1 >= 0:
                is_legal_move = self.__is_legal_move(row - 1, col + 2,
                                                     opposite_color)[0]
                if is_legal_move:
                    moves.append((row - 1, col + 2))
            if row + 1 < 8:
                is_legal_move = self.__is_legal_move(row + 1, col + 2,
                                                     opposite_color)[0]
                if is_legal_move:
                    moves.append((row + 1, col + 2))

        return self.__get_list_of_moves_helper(row, col, moves)

    def __all_possible_moves_queen(self, row: int,
                                   col: int, opposite_color) -> List[Move]:
        """
        This function computes all possible and legal moves for queen that is
        currently in cell with (row, col).
        :param row: int, the current row of the queen.
        :param col: int, the current col of the queen.
        :param opposite_color: color, the opponents color.
        :return: List[Move], list of all possible and legal moves for queen.
        """
        moves = self.__all_possible_moves_rook(row, col, opposite_color)
        moves += self.__all_possible_moves_bishop(row, col, opposite_color)
        return moves

    def __all_possible_moves_king(self, row: int,
                                  col: int, opposite_color) -> List[Move]:
        """
        This function computes all possible and legal moves for king that is
        currently in cell with (row, col).
        :param row: int, the current row of the king.
        :param col: int, the current col of the king.
        :param opposite_color: color, the opponents color.
        :return: List[Move], list of all possible and legal moves for king.
        """

        def add_moves(_row, _col, _opposite_color):
            _moves = []
            for i in range(_col - 1, _col + 2):
                try:
                    if self.__is_legal_move(_row, i, _opposite_color)[0]:
                        _moves.append((_row, i))
                except Exception as e:
                    print(e)
            return _moves

        moves = []
        if row - 1 >= 0:
            moves += add_moves(row - 1, col, opposite_color)
        if row + 1 < 8:
            moves += add_moves(row + 1, col, opposite_color)

        if col - 1 >= 0:
            if self.__is_legal_move(row, col - 1, opposite_color)[0]:
                moves.append((row, col - 1))

        if col + 1 >= 0:
            if self.__is_legal_move(row, col + 1, opposite_color)[0]:
                moves.append((row, col + 1))

        return self.__get_list_of_moves_helper(row, col, moves)

    def get_all_possible_moves(self, row: int, col: int) -> List[Move]:
        """
        This function computes and returns all possible and legal moves
        for selected cell on (row, col)
        :param row: int, row on the board.
        :param col: int, col on the board.
        :return: List[Move] all possible moves that can be done from cell on
        (row, col).
        """
        piece = self.get_piece_at(row, col)

        if piece == Pieces.BLACK_PAWN:
            return self.__all_possible_moves_pawn(row, col, Colors['WHITE'])
        elif piece == Pieces.WHITE_PAWN:
            return self.__all_possible_moves_pawn(row, col, Colors['BLACK'])

        if piece == Pieces.BLACK_BISHOP:
            return self.__all_possible_moves_bishop(row, col, Colors['WHITE'])
        elif piece == Pieces.WHITE_BISHOP:
            return self.__all_possible_moves_bishop(row, col, Colors['BLACK'])

        if piece == Pieces.BLACK_ROOK:
            return self.__all_possible_moves_rook(row, col, Colors['WHITE'])
        elif piece == Pieces.WHITE_ROOK:
            return self.__all_possible_moves_rook(row, col, Colors['BLACK'])

        if piece == Pieces.BLACK_HORSE:
            return self.__all_possible_moves_horse(row, col, Colors['WHITE'])
        elif piece == Pieces.WHITE_HORSE:
            return self.__all_possible_moves_horse(row, col, Colors['BLACK'])

        if piece == Pieces.BLACK_QUEEN:
            return self.__all_possible_moves_queen(row, col, Colors['WHITE'])
        elif piece == Pieces.WHITE_QUEEN:
            return self.__all_possible_moves_queen(row, col, Colors['BLACK'])

        if piece == Pieces.BLACK_KING:
            return self.__all_possible_moves_king(row, col, Colors['WHITE'])
        elif piece == Pieces.WHITE_KING:
            return self.__all_possible_moves_king(row, col, Colors['BLACK'])

        return []

    def move_piece(self, move: Move) -> bool:
        """
        This function responsible for performaing logical piece movement

        Note: The main assumption is the move variable holds Move that is
        constructed by means of this class and thus is is legal move to be
        performed. If you supply this function a move that is not legal move
        then we it may have undefined behaviour.

        :param move: Move object, holds the move that should be performed.
        :return: True, if and only if the King was killed as a result of move.
        """
        from_row = move['from_row']
        from_col = move['from_col']
        to_row = move['to_row']
        to_col = move['to_col']
        from_piece = move['from_piece']
        to_piece = move['to_piece']
        self.set_piece_at(to_row, to_col, from_piece)
        self.set_piece_at(from_row, from_col, Pieces.NONE)
        self.move_stack.append(move)
        if to_piece != Pieces.NONE:
            self.total_material[to_piece] -= 1
        if to_piece == Pieces.WHITE_KING or to_piece == Pieces.BLACK_KING:
            return True
        return False

    def undo_move(self) -> Move:
        """
        This function undos' the last move that was performed. The operation
        here is very similar to stack operation of pop. It pops the last move
        from the board.
        :return: Move object that strores the last move that was made on board.
        """
        last_move = self.move_stack.pop()
        self.set_piece_at(last_move['from_row'],
                          last_move['from_col'],
                          last_move['from_piece'])
        self.set_piece_at(last_move['to_row'],
                          last_move['to_col'],
                          last_move['to_piece'])
        if last_move['to_piece'] != Pieces.NONE:
            self.total_material[last_move['to_piece']] += 1
        return last_move

    def evaluation_function(self) -> int:
        """
        This function is responsible to compute the current score of the board.
        It is used for AI purposes.
        :return: int, the score of the board.
        """

        king_difference = self.total_material[Pieces.WHITE_KING] - \
                          self.total_material[Pieces.BLACK_KING]

        queen_difference = self.total_material[Pieces.WHITE_KING] - \
                           self.total_material[Pieces.BLACK_KING]

        rook_difference = self.total_material[Pieces.WHITE_ROOK] - \
                          self.total_material[Pieces.BLACK_ROOK]

        bishop_difference = self.total_material[Pieces.WHITE_BISHOP] - \
                            self.total_material[Pieces.BLACK_BISHOP]

        knight_difference = self.total_material[Pieces.WHITE_HORSE] - \
                            self.total_material[Pieces.BLACK_HORSE]

        pawn_difference = self.total_material[Pieces.WHITE_PAWN] - \
                          self.total_material[Pieces.BLACK_PAWN]

        total_balance = (200 * king_difference + 50 * queen_difference +
                         5 * rook_difference + 3 + bishop_difference +
                         3 * knight_difference + 1 * pawn_difference)

        return total_balance


class DisplayBoard:
    """ This class is the 'view' of the board. It handles all of the visual
    logic of the board. It translates the logical board (of type Board) into the
    visual board. """

    def __init__(self, destination: pygame.Surface, board: Board):
        """
        This function is default c'tor and it loads the pieces and other
        graphics relevant to the board.
        """
        self.pieces_graphics = Pieces.load_pieces()
        self.destination = destination
        self.board = board

    def draw_cell(self, row: int, col: int) -> None:
        """
        This cell performs visual draws specific cell given by coordinates of
        (row, col).
        :param row: int, the row of specific cell.
        :param col: int, the col of specific cell.
        :return: None.
        """
        pygame.draw.rect(self.destination,
                         self.board.get_cell_color_at(row, col),
                         [col * BoardNode.CELL_HEIGHT,
                          row * BoardNode.CELL_WIDTH,
                          BoardNode.CELL_WIDTH,
                          BoardNode.CELL_HEIGHT])
        piece = self.board.get_piece_at(row, col)
        if piece != Pieces.NONE:
            self.destination.blit(self.pieces_graphics[piece],
                                  (col * BoardNode.CELL_HEIGHT,
                                   row * BoardNode.CELL_WIDTH))

    def show_board(self):
        """
        This function responsible to show the entire row on the screen.

        Important note: Currently this function works well when user is white
        and computer is black. It should be extended to all cases.

        :return: None.
        """
        for row in range(0, BoardParameters['ROWS']):
            for col in range(0, BoardParameters['COLS']):
                pygame.draw.rect(self.destination,
                                 self.board.get_cell_color_at(row, col),
                                 [col * BoardParameters['CELL_WIDTH'],
                                  row * BoardParameters['CELL_HEIGHT'],
                                  BoardParameters['CELL_WIDTH'],
                                  BoardParameters['CELL_HEIGHT']])
                piece = self.board.get_piece_at(row, col)
                if piece != Pieces.NONE:
                    self.destination.blit(self.pieces_graphics[piece],
                                          (col * BoardParameters['CELL_HEIGHT'],
                                           row * BoardParameters['CELL_WIDTH']))
        pygame.display.update()

    def display_selected(self, row: int, col: int, move_type) -> None:
        """
        This function is responsible to display selected square.
        :param row: int, the row of specific cell.
        :param col: int, the col of specific cell.
        :param move_type:
        :return: None
        """
        color = Colors['BLUE']
        if move_type == MoveType['POSSIBLE_MOVE']:
            color = Colors['GREEN']
        pygame.draw.rect(self.destination,
                         color,
                         [col * BoardNode.CELL_WIDTH + 5,
                          row * BoardNode.CELL_HEIGHT + 5,
                          BoardNode.CELL_WIDTH - 10,
                          BoardNode.CELL_HEIGHT - 10], 5)
        pygame.display.update()

    def display_all_possible_moves(self, moves: List[Move]) -> None:
        """
        This function responsible to visualise all possible moves to the user.
        :param moves: List[Moves], list of all possible and legal moves.
        :return: None
        """
        for move in moves:
            self.display_selected(move['to_row'],
                                  move['to_col'],
                                  MoveType['POSSIBLE_MOVE'])
        pygame.display.update()

    def unselect(self, row: int, col: int, moves: List[Move]) -> None:
        """
        This function responsible for the visual logic of unselecting cell.
        :param row: int, is the row of cell to be unselected.
        :param col: int, is the col of cell to be unselected.
        :param moves: List[Moves], represents the possible moves.
        :return: None
        """
        self.draw_cell(row, col)
        for move in moves:
            row = move['to_row']
            col = move['to_col']
            self.draw_cell(row, col)
        pygame.display.update()

    def move_piece(self, move: Move, moves: List[Move]) -> None:
        """
        This function responsible for handling the visual logic of piece
        movement.
        :param move: Move, is the move that should be displayed.
        :param moves: List[Moves] is the list of all moves that should be
        unselected visually as result of move.
        :return: None
        """
        from_row = move['from_row']
        from_col = move['from_col']
        to_row = move['to_row']
        to_col = move['to_col']
        self.unselect(from_row, from_col, moves)
        self.draw_cell(from_row, from_col)
        self.draw_cell(to_row, to_col)
        pygame.display.update()

    def undo_move(self, last_move: Move):
        """
        This function responsible for visual logic of undo move.
        :param last_move: Move, is the move that should be displayed.
        :return None
        """
        self.move_piece(last_move, [])
