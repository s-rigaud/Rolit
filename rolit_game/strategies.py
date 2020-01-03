"""
This module contains different strategies which allow the AI
to be able to play randomly or using the optimal move based
on Minimax algorithm with multiple levels of foresight
"""

from abc import ABC, abstractmethod
from random import choice
from math import inf as infinity
from copy import deepcopy
from itertools import product

from rolit_game.helpers import compute_distance, test_cell_existence, exist_adjacent_cell

class AI_Strategy(ABC):
    """Abstract base class for all strategies of the artificial inteligences
    """
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'AI is currently using {self.name} strategy'

    @abstractmethod
    def play(self, board: list):
        """ ABstract method which define the playing behaviour
        """

    def get_playable_cells(self, board: list) -> list:
        """Return all cells with a surrounding coin
        """
        all_playable_cells = []
        for i, line in enumerate(board):
            for j, _ in enumerate(line):
                if board[i][j] == 0 and exist_adjacent_cell(board, (i, j)):
                    all_playable_cells.append((i, j))
        return all_playable_cells


class RandomlyPlayStrategy(AI_Strategy):
    """AI Strategic class playing randomly
    """
    def __init__(self):
        AI_Strategy.__init__(self, 'Randomly Play')

    def play(self, board: list) -> tuple:
        """Return the indexof a random empty cell
        """
        return choice(self.get_playable_cells(board))


class MiniMaxStrategy(AI_Strategy):
    """ AI Strategic class playing using the minimax algorithm
    """
    def __init__(self, pseudo_level: str, player_value: int, opponent_value: int):
        """Initializing the level of the ai following the choosen one
        """
        AI_Strategy.__init__(self, 'MiniMax')
        self.player_value = player_value
        self.opponent_value = opponent_value
        levels = {'Medium':1, 'Hard':2, 'Expert':3}
        self.level = levels.get(pseudo_level)
        if self.level is None:
            raise AttributeError('AI level should be set to medium, hard or expert')

    def play(self, board: list) -> tuple:
        """Return the best cell returned from the minimax algorithm
        """
        best_move = self.minimax(board, self.level, self.player_value, self.player_value, self.opponent_value)
        return (best_move[0], best_move[1])

    def evaluate(self, board: list, player: int, opponent: int) -> int:
        """Return the value of a specific board
        ∑ (coins of computer) - ∑ (coins of player)
        """
        return self.count_coins(player, board) - self.count_coins(opponent, board)

    def check_changing_colors(self, board: list, index_initial_cell_filled: tuple, player: int) -> list:
        """Check if a coin need to be rolled to an other color
        """

        #Each time the result is [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        possible_lines = list(filter(lambda x: x[0] != 0 or x[1] != 0, list(product(range(-1, 2), range(-1, 2)))))

        for coords in possible_lines:
            stack = []
            roll_needed = False
            while True:
                a = index_initial_cell_filled[0] + coords[0] * (len(stack)+1)
                b = index_initial_cell_filled[1] + coords[1] * (len(stack)+1)
                # print('Other cell: ({},{})'.format(a,b))

                if a < 0 or a > len(board)-1 or b < 0 or b > len(board)-1 or board[a][b] == 0:
                    break
                elif board[a][b] == player:
                    roll_needed = True
                    break

                stack.append((a, b))

            if roll_needed:
                for cell_index in stack:
                    board[cell_index[0]][cell_index[1]] = player

        return board

    def count_coins(self, coin_value: int, board: list):
        """Count the number of coins like
        """
        return sum([line.count(coin_value) for line in board])

    def minimax(self, board: list, depth: int, asked_by: int, player: int, opponent: int,
                alpha_boundary: int = 1000, beta_boundary: int = 1000) -> tuple:
        """Implementation of the MiniMax Algorithm to return one of the best playable move
        """
        # import ipdb;ipdb.set_trace()
        # TODO : IMPLEMENT ALPHA-BETA pruning

        # If the board is full or if the depth is reached we return the value of the turn
        # Need tocheck boundaries
        if depth == 0 or not self.get_playable_cells(board):
            if asked_by == player:
                score = self.evaluate(board, asked_by, opponent)
            else:
                score = self.evaluate(board, asked_by, player)
            return [-1, -1, score]

        all_moves = []

        #For each cell on the board we try to compute the turn with the highest value
        for cell in self.get_playable_cells(board):
            x, y = cell[0], cell[1]

            temp_board = deepcopy(board)
            temp_board[x][y] = player
            temp_board = self.check_changing_colors(temp_board, (x, y), player)

            if player == asked_by:
                score = self.minimax(temp_board, depth - 1, asked_by, opponent, player)
            else:
                score = self.minimax(temp_board, depth - 1, asked_by, opponent, player)

            #Assign the given score to the coordinates of the cell placed
            score[0], score[1] = x, y

            all_moves.append(score)

        print(f'All moves : {all_moves}')
        if player == asked_by:
            #Return one of the random best moves chosen randomly
            maxScore = max([move[2] for move in all_moves])
            all_best_moves = list(filter(lambda x: x[2] == maxScore, all_moves))
            print(f'All best moves : {all_best_moves}')
            return choice(all_best_moves)
        else:
            minScore = min([move[2] for move in all_moves])
            all_worst_moves = list(filter(lambda x: x[2] == minScore, all_moves))
            print(f'All worst moves : {all_worst_moves}')
            return choice(all_worst_moves)
