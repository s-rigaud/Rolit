

import pygame
from math import inf as infinity

from rolit_game.helpers import compute_distance

# Slow loading done before displaying any UI
pygame.init()
pygame.font.init()

class UI:

    def __init__(self, board_size: int):
        self._dict_size = {'x_margin': 48, 'y_margin': 48, 'x_gap': 85, 'y_gap': 85}
        self.green_coin = pygame.image.load("rolit_game/images/greenCoin.png")
        self.red_coin = pygame.image.load("rolit_game/images/redCoin.png")
        self.dead_cell = pygame.image.load("rolit_game/images/deadCell.png")
        self.icon = pygame.image.load("rolit_game/images/deadCell.ico")
        self.board_img = pygame.image.load(f'rolit_game/images/board_{board_size}x{board_size}.png')

        self.board_width: int
        self.board_height: int
        self.board_width, self.board_height = self.board_img.get_size()

        self.screen = pygame.display.set_mode((self.board_width, self.board_height))
        self.screen.blit(self.board_img, (0, 0))
        self.update_ui()

        self.cell_positions = []
        for i in range(board_size):
            x = i * self._dict_size['x_gap'] + self._dict_size['x_margin']
            self.cell_positions.append([])
            for j in range(board_size):
                y = j * self._dict_size['y_gap'] + self._dict_size['y_margin']
                self.cell_positions[i].append((x, y))

        self.font_score = pygame.font.SysFont('Comic Sans MS', 25)
        pygame.display.set_caption('Rolit Game')
        pygame.display.set_icon(self.icon)

    def update_ui(self):
        """Update and display the board
        """
        pygame.display.flip()

    def cell_index_from_pos(self, cell_pos: tuple):
        """Get the index of a cell passing its coordonates
        Swapping axes because the coordinate system  X/Y for the mouse isn't the same as row/columns
        ----→ mouseX                   ------→ column
        |                              |
        |                 →  →  →  →   |
        ↓                              ↓
        mouseY                         row
        """
        i = int((cell_pos[0] - self._dict_size['x_margin']) / self._dict_size['x_gap'])
        j = int((cell_pos[1] - self._dict_size['y_margin']) / self._dict_size['y_gap'])
        return (j, i)

    def pos_from_cell_index(self, cell_index: tuple) -> tuple:
        """Get the position of a cell passing its indexes
        """
        x = cell_index[0] * self._dict_size['x_gap'] + self._dict_size['x_margin']
        y = cell_index[1] * self._dict_size['y_gap'] + self._dict_size['y_margin']
        return (x, y)

    def get_nearest_cell(self) -> tuple:
        """Find the nearest cell from the position of the mouse
        """
        x, y = self.get_pos_mouse()
        nearest_cell = None
        shortest_distance = +infinity

        for rowLocation in self.cell_positions:
            for location in rowLocation:
                dist = compute_distance((x, y), location)
                if dist < shortest_distance:
                    nearest_cell = location
                    shortest_distance = dist
        return nearest_cell

    def get_pos_mouse(self) -> tuple:
        """Return the position of the mouse
        """
        x, y = pygame.mouse.get_pos()
        return (x, y)

    def update_diplay(self, board: list, scores: list):
        """ Refresh the all UI (Board + Score)
        """
        self.screen.blit(self.board_img, (0, 0))
        for i in range(len(board)):
            for j in range(len(board)):
                if board[i][j] == 1:
                    self.add_coin_img(self.red_coin, self.pos_from_cell_index((j, i)))
                elif board[i][j] == 2:
                    self.add_coin_img(self.green_coin, self.pos_from_cell_index((j, i)))
                elif board[i][j] == 100:
                    self.add_coin_img(self.dead_cell, self.pos_from_cell_index((j, i)))

        textsurface = self.font_score.render(f'{scores[0]} - {scores[1]}', False, (150, 150, 150))
        self.screen.blit(textsurface, (self.board_width-70, self.board_height-30))

        self.update_ui()

    def add_coin_img(self, img: pygame.Surface, pos: tuple):
        """Place a coin image on the board
        """
        x, y = pos
        x -= img.get_size()[0] / 2
        y -= img.get_size()[1] / 2
        self.screen.blit(img, (x, y))

        self.update_ui()