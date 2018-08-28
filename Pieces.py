import pygame
from Consts import Colors


class Pieces:
    BLACK_PAWN = "black_pawn.png"
    BLACK_HORSE = "black_horse.png"
    BLACK_BISHOP = "black_bishop.png"
    BLACK_ROOK = "black_rook.png"
    BLACK_QUEEN = "black_queen.png"
    BLACK_KING = "black_king.png"
    WHITE_PAWN = "white_pawn.png"
    WHITE_HORSE = "white_horse.png"
    WHITE_BISHOP = "white_bishop.png"
    WHITE_ROOK = "white_rook.png"
    WHITE_QUEEN = "white_queen.png"
    WHITE_KING = "white_king.png"
    NONE = "None"

    @staticmethod
    def get_list_of_pieces():
        return [
            Pieces.BLACK_PAWN,
            Pieces.BLACK_HORSE,
            Pieces.BLACK_BISHOP,
            Pieces.BLACK_ROOK,
            Pieces.BLACK_QUEEN,
            Pieces.BLACK_KING,
            Pieces.WHITE_PAWN,
            Pieces.WHITE_HORSE,
            Pieces.WHITE_BISHOP,
            Pieces.WHITE_ROOK,
            Pieces.WHITE_QUEEN,
            Pieces.WHITE_KING,
            Pieces.NONE
        ]

    @staticmethod
    def load_pieces():
        dic = {}
        for piece in Pieces.get_list_of_pieces():
            if piece != Pieces.NONE:
                dic[piece] = pygame.image.load('./chess_pieces/' + piece)
        return dic

    @staticmethod
    def get_piece_color(piece):
        """ 
        This function takes in piece and returns its color. 
        :param: piece, is the piece. 
        :return: Color of the piece. 
        """
        if  piece == Pieces.BLACK_BISHOP or \
            piece == Pieces.BLACK_HORSE or \
            piece == Pieces.BLACK_KING or \
            piece == Pieces.BLACK_PAWN or \
            piece == Pieces.BLACK_QUEEN or \
            piece == Pieces.BLACK_ROOK:
            return Colors['BLACK']
        return Colors['WHITE']

