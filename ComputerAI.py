from random import randint
from Move import Move
from Consts import Colors, BoardParameters
from typing import List, Tuple
from Board import Board
from operator import itemgetter


class ComputerAI:
    """ This class is responsible for the AI of the computer. """

    def __init__(self, difficulty,
                 computer_color=Colors['BLACK'],
                 user_color=Colors['WHITE']):
        """
        Default c'tor.
        :param difficulty: int, indicates the depth of the search tree in the
        minmax algorithm.
        :param computer_color: the color of the computer player.
        :param user_color: the color of the user player.
        """
        self.__difficulty = difficulty
        self.user_color = user_color
        self.computer_color = computer_color

    def minmax_algorithm(self,
                         board: Board,
                         current_move_color: Colors,
                         next_move_color:
                         Colors,
                         tree_depth: int,
                         is_min: bool) -> List[Tuple[Move, int]]:
        """
        This function is the minmax-algorithm for computing the best move.

        How the algorithm works?
        ------------------------

        We can consider the chess game as zero-sum game. The zero-sum games 
        are games where each participant's gain or loss of utility is exactly 
        balanced by the losses or gains of the utility of the other participants
        If the total gains of the participants are added up and total losses are 
        subtracted, they will sum to zero.

        The Board object has special function which is responsible to evaluate 
        the board in terms of zero-sum game. If the position of the board is 
        neutral then the result of the evaluation result in zero (for example 
        when we are at the beginning of the game). Otherwise, if white leads 
        then the score will be positive and if black leads then the score will 
        be negative.

        From that logic we may see that white main interest is make a move such 
        that **maximizes** the evaluation of the board on the next position. For 
        example, if white has the option to perform three moves which lead into 
        next results:
            
            Move1: evaluation of 3
            Move2: evaluation of 5
            Move3: evaluation of 0
        
        It will prefer to perform {Move2} because this will result in the 
        maximum score for the next position. Maximum score white means that it 
        will be the less good move black. The same goes for black. Black will 
        always like to  make move that **minimizes** the evaluation of the 
        board. Minimizing the score of the board means that it minimizes the 
        position for white player, thus increases his chances to win.
        
        
        Idea behind the implementation of the algorithm.
        ------------------------------------------------
        
        The main idea is to construct tree with the indicated depth, and on each 
        level of the tree we will select what move to make with respect to the 
        player that plays that move. So, for simple example, consider the black 
        should make the next move. But, it should make the best move without 
        looking further. As we said previously, for each move of black, he will 
        try to minimize the score of the board.
        
        This is how the tree will look.  
        
               (B)
                |
            1---2---3
            
        Black has three moves to make {#1, #2, #3}. For each such move we should 
        evaluate the score of the board and choose one that minimizes that 
        score.  
        
        Now, consider more complex example where black is about to play and he 
        must to look one move forward. In human perspective this means that he 
        thinks not only about his move but also about the response of the 
        opponent. On such case, the tree may look as follows: 
        
                            (B)
                             |
                    1--------2---------3
                    |        |         |
                 a--b--c  e--d--f   g--h--i
                
        How do we think about that tree? Black is about to make the move, it is 
        why (B) is on the root, and it has three options to perform that move: 
        {#1, #2, #3}. For each such option, white may respond. For example, if 
        black decides to go with move #1, then white may respond with moves 
        {'a', 'b', 'c'}. Black should think about the response and take into the 
        count. For each move of black, the white will perform move that max 
        board score. For example, consider that for move #1 then whites best 
        move is 'a', for move #2 whites best move is 'd', and finally for move 
        #3 whites best move is 'i'. For each such sequence (#1->'a'), (#2->'d'), 
        (#3->'i') we will score the board, and we will choose the move that will 
        have the minimal score.  
              
                
        Special notes about current implementation:
        -------------------------------------------

        First of all, note that this algorithm is recursive algorithm so it is 
        probably will not be an efficient solution for very deep computations. 
        Second, currently algorithm version is the **basic** one of minmax. This 
        means it has no optimization or alpha-beta pruning to make performance 
        better. Thus, this algorithm is in efficient version of the AI, and 
        should be optimized any soon.

        Currently, it works very well for 4-6 moves into the deep.

        :param board: the logical representation of the board, Board object.
        
        :param current_move_color: it is the color of the current player to move
        in {Colors['BLACK'], Colors['WHITE']}.
        
        :param next_move_color: it is the color of the next player to move, in 
        {Colors['BLACK'], Colors['WHITE']}.
        
        :param tree_depth: the number of moves to compute forward. For example, 
        tree_depth = 0 it means that we compute only one move forward, and 
        tree_depth = 1 it means that we compute 2 moves forward. The variable 
        must be even number (black, white, black, white, black, white ...).
        
        :param is_min: flag (either True, or False) required to determine 
        whether we minimize or maximize the move.
        
        :return: list of best moves to perform.
        """

        moves = []  # type: List[Tuple[Move, int]]
        for row in range(0, BoardParameters['ROWS']):
            for col in range(0, BoardParameters['COLS']):
                if board.get_piece_color_at(row, col) == current_move_color:
                    all_moves = board.get_all_possible_moves(row, col)
                    for move in all_moves:
                        board.move_piece(move)
                        if tree_depth == 0:
                            moves.append((move, board.evaluation_function()))
                        else:
                            best_moves = \
                                self.minmax_algorithm(board, next_move_color,
                                                      current_move_color,
                                                      tree_depth - 1,
                                                      not is_min)
                            moves.append((move, best_moves[0][1]))
                        board.undo_move()

        min_score = min(moves, key=itemgetter(1))[1]
        max_score = max(moves, key=itemgetter(1))[1]

        if is_min:
            return [move for move in moves if move[1] == min_score]
        return [move for move in moves if move[1] == max_score]

    def computers_play(self, board: Board) -> Move:
        """
        Compute the best move for the computer.
        :param board: the logical representation of the board, a Board object.
        :return: The best move possible.
        """
        best_moves = self.minmax_algorithm(board, self.computer_color,
                                           self.user_color, self.__difficulty,
                                           True)
        move = best_moves[randint(0, len(best_moves) - 1)]
        return move[0]
