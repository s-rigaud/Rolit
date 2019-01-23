"""
"""

from math import sqrt
from itertools import product

def compute_distance(fisrt_point: tuple, second_point: tuple) -> float:
    """Compute the distance between two positions
    """
    return sqrt(int(fisrt_point[0] - second_point[0])**2 + int(fisrt_point[1] - second_point[1])**2)

def test_cell_existence(board: list, i: int, j: int) -> bool:
    """Check if the cell exists on the board
    """
    return not (i < 0 or i > len(board)-1 or j < 0 or j > len(board)-1)


def exist_adjacent_cell(board: list, cell_index: tuple) -> bool:
    """Test to know if there is a coin in the surrounding cells
    """
    #Each time the result = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    possible_cells_direction = list(filter(lambda x: x[0] != 0 or x[1] != 0, list(product(range(-1, 2), range(-1, 2)))))

    for coord_couple in possible_cells_direction:
        i = cell_index[0] + coord_couple[0]
        j = cell_index[1] + coord_couple[1]

        if not test_cell_existence(board, i, j):
            continue

        # If a cell isn't empty
        if board[i][j] != 0:
            return True
    return False