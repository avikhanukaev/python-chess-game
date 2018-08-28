from typing import List


class Move:
    """
    This class is responsible to describe object that stores the move.
    Each move consist out of four parts. The first one is the initial
    coordinates of the piece - thus, the place on board where the piece were and
    from where it is moved. Second, is the target coordinates - thus, the place
    on board to where the piece should be moved. The third, is the piece that is
    been moved, and the fourth is the pieced that was eaten as result of the
    move.
    """

    def __init__(self, from_row, from_col, to_row,
                 to_col, from_piece, to_piece):
        """
        Default c'tor.
        :param from_row: int, the initial row.
        :param from_col: int, the initial col.
        :param to_row:  int, the target row.
        :param to_col:  int, the target col.
        :param from_piece:  the piece tht should be moved.
        :param to_piece: the piece that was eaten as a result of the move.
        """
        self.__from_row = from_row
        self.__from_col = from_col
        self.__to_row = to_row
        self.__to_col = to_col
        self.__from_piece = from_piece
        self.__to_piece = to_piece

    def get_from_cell(self) -> List[int]:
        """
        :return: this function return list of form [row, col] that describes the
        initial board coordinates of the piece.
        """
        return [self.__from_row, self.__from_col]

    def get_to_cell(self) -> List[int]:
        """
        :return: this function return list of form [row, col] that describes the
        target board coordinates of the piece.
        """
        return [self.__to_row, self.__to_col]

    def get_from_piece(self):
        """
        :return: this function returns the piece that is moved in the move.
        """
        return self.__from_piece

    def get_to_piece(self):
        """
        :return: this function returns the piece that was eaten as result of the
        move.
        """
        return self.__to_piece

    def __getitem__(self, key):
        """
        This function allows us to treat the object as dictionary.
        :param key: the key of query. For example, {'from_row', 'from_col',
        'to_row', 'to_col', 'from_piece', 'to_piece'}
        :return: returns the required information.
        """
        if key == 'from_row':
            return self.__from_row
        elif key == 'from_col':
            return self.__from_col
        elif key == 'to_row':
            return self.__to_row
        elif key == 'to_col':
            return self.__to_col
        elif key == 'from_piece':
            return self.__from_piece
        elif key == 'to_piece':
            return self.__to_piece
        return None

    def __repr__(self):
        return str(self)

    def __str__(self):
        return '{ From: ' + self.__from_piece + \
               ' at ' + str(self.get_from_cell()) + ' | ' + \
               'To: ' + self.__to_piece + ' at ' + str(self.get_to_cell()) + '}'

    def __eq__(self, other):
        return self.get_from_cell() == other.get_from_cell() and \
               self.get_to_cell() == other.get_to_cell() and \
               self.get_from_piece() == other.get_from_piece() and \
               self.get_to_piece() == other.get_to_piece()
