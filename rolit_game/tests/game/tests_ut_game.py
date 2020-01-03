import time
import unittest

import rolit_game


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        """Call before each test
        """
        g = Game()
        g.config('5x5', 'Player-AI', 'Medium')

    def test_line_format_init_board_lists(self):
        g._init_board_lists()
        for line in g.board:
            self.assertEqual(g.board_size, len(line))

    def test_init_board_lists(self):
        g._init_board_lists()
        self.assertEqual(g.board, [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]])

    def test_place_dead_cells(self):
        g._init_board_lists()
        g._place_dead_cells()
        nb_dead_cell = sum((line.count(g.dead_coin_value) for line in g.board))
        self.assertTrue(nb_dead_cell)


def test_play():
    pass
def test_display():
    pass
def test_get_nearest_cell():
    pass
def test_place_coin():
    pass
def test_ai_play():
    pass
def test_check_changing_colors():
    pass
def test_existing_cell():
    pass
def test_switch_turn():
    pass
def test_cell_index_from_pos():
    pass
def test_pos_from_cell_index():
    pass
def test_add_score():
    pass
def test_add_img_coin():
    pass
def test_roll():
    pass
def test_exist_adjacent_cell():
    pass
def test_count_score():
    pass


if __name__ == '__main__':
    unittest.main()