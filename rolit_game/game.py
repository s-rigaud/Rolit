""" Main file responsible for the game organisation
"""

import sys
from time import sleep
from itertools import product
import pygame

from rolit_game.ui import UI
from rolit_game.popup import Popup
from rolit_game.helpers import test_cell_existence, exist_adjacent_cell
from rolit_game.strategies import AI_Strategy, RandomlyPlayStrategy, MiniMaxStrategy

class Game:
    """Main manager for the game
    """
    def __init__(self):
        self.ui_settings = None

        self.board_size: int
        self.board = []

        self._PLAYER1 = 1
        self.score1 = 0
        self._PLAYER2 = 2
        self.score2 = 0
        self.turn = self._PLAYER1
        self.beginner = self._PLAYER1

        self.gamemode: str
        self.ai_level: str
        self.ai_strategy: AI_Strategy

        # Time intervall between two actions (making the AI pause between two moves)
        self._SLEEP_TIME = 0.3

    def play(self):
        """Main function of the game
        """
        while not self.end_game:
            if self.gamemode == "AI-AI":
                sleep(self._SLEEP_TIME)
                cell_pos = self.ai_play()
                if not self.place_coin(cell_pos):
                    print('The AI return a non valid cell')
                self.check_changing_colors(cell_pos)
                self.ui_settings.update_diplay(self.board, self.scores)
                self.switch_turn()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        cell_pos = self.ui_settings.get_nearest_cell()
                        # While he/she didn't play in a valid empty cell
                        if not self.place_coin(cell_pos):
                            break
                        self.check_changing_colors(cell_pos)
                        self.ui_settings.update_diplay(self.board, self.scores)
                        self.switch_turn()

                        if self.gamemode != "Player-Player" and not self.end_game:
                            sleep(self._SLEEP_TIME)
                            cell_pos = self.ai_play()
                            if not self.place_coin(cell_pos):
                                print('The AI return a non valid cell')
                            self.check_changing_colors(cell_pos)
                            self.ui_settings.update_diplay(self.board, self.scores)

                            self.switch_turn()
                    if event.type == pygame.QUIT:
                        sys.exit()

        self.score1, self.score2 = self.scores
        sleep(self._SLEEP_TIME)

        need_to_save_score = self.gamemode == "Player-AI" and self.board_size == 5
        play_again = Popup.display_score(self.score1, self.score2, self.ai_level, need_to_save_score)

        # If the player want to play again
        if play_again:
            # Initialize the new game with the old configuration
            self.config(self.board_size, self.gamemode, self.ai_level)

            # If its a game with AI -> The beginner of the game change,
            # The AI play one turn and the play function is called
            if self.gamemode != "Player-Player":
                if self.beginner == self._PLAYER1:
                    self.beginner = self._PLAYER2
                    #back to green
                    self.switch_turn()
                    self.place_coin(self.ai_play())
                    self.check_changing_colors(cell_pos)
                    #back to red
                    self.switch_turn()
                else:
                    self.beginner = self._PLAYER1
                    #Back to red
                    self.switch_turn()

            self.play()

    def config(self, board_size: int, gamemode: str, ai_level: str):
        """Load the default board and display it
        """
        self.board_size = board_size
        self.ui_settings = UI(self.board_size)

        # Reseting values
        self.board.clear()
        self._init_board_lists()

        # Placing some dark coins to allow the game to be fair
        self._place_dead_cells()
        self.ui_settings.update_ui()

        self.score1 = 0
        self.score2 = 0
        self.ai_level = ai_level

        self.gamemode = gamemode
        if self.gamemode != "Player-Player":
            self.ai_strategy = self.get_ai_strategy(ai_level, self._PLAYER2, self._PLAYER1)
            if self.gamemode == "AI-AI":
                strat2 = self.get_ai_strategy(ai_level, self._PLAYER1, self._PLAYER2)
                self.ai_strategy = (strat2, self.ai_strategy)
            print(self.ai_strategy)

    def get_ai_strategy(self, ai_level: str, player: int, opponent: int):
        if ai_level == "Easy":
            return RandomlyPlayStrategy()
        elif ai_level in ["Medium", "Hard", "Expert"]:
            return MiniMaxStrategy(ai_level, self._PLAYER2, self._PLAYER1)

    def _init_board_lists(self):
        """Fill the board with zeros
        """
        for i in range(self.board_size):
            self.board.append([])
            [self.board[i].append(0) for y in range(self.board_size)]

    def _place_dead_cells(self):
        """Place a black cell which allow the game to be fair
        """
        list_dead_cells = [(2, 2)] if self.board_size == 5 else [(4, 4), (3, 3)]
        for pos in list_dead_cells:
            cell_pos = self.ui_settings.pos_from_cell_index(pos)
            if self.board[pos[0]][pos[1]] == 0:
                self.ui_settings.add_coin_img(self.ui_settings.dead_cell, cell_pos)
                self.board[pos[0]][pos[1]] = 100
            else:
                print('Cell already full - Coords : {} , {}'.format(pos[0], pos[1]))

    def place_coin(self, cell_pos: tuple) -> tuple:
        """Place a coin in a valid cell
        """
        i, j = self.ui_settings.cell_index_from_pos(cell_pos)
        if exist_adjacent_cell(self.board, (i, j)):
            if self.board[i][j] == 0:
                if self.turn == self._PLAYER1:
                    self.ui_settings.add_coin_img(self.ui_settings.red_coin, cell_pos)
                else:
                    self.ui_settings.add_coin_img(self.ui_settings.green_coin, cell_pos)
                self.board[i][j] = self.turn
                # print('Cell placed - Coords : {} , {} by {}'.format(i,j,self.turn))
                return True
            # TODO : Add specific error ?
            print('Cell already full {} - Coords : {} , {}'.format(self.turn, i, j))
        if self.gamemode == "Player-Player":
            Popup.place_near_coin()
        return False

    def ai_play(self) -> tuple:
        """ Play randomly on an empty cell near an other coin
        """
        if self.gamemode == "AI-AI":
            if self.turn == self._PLAYER1:
                cell_index = self.ai_strategy[0].play(self.board)
            else:
                cell_index = self.ai_strategy[1].play(self.board)
        else:
            cell_index = self.ai_strategy.play(self.board)
        inversed_cell_pos = self.ui_settings.pos_from_cell_index(cell_index)
        cell_pos = (inversed_cell_pos[1], inversed_cell_pos[0])

        return cell_pos

    def check_changing_colors(self, cell_pos: tuple):
        """Check if some coins near the last coin placed need to be roll and roll them after
        """
        index_initial_cell_filled = self.ui_settings.cell_index_from_pos(cell_pos)

        # get the eight coordinates to add from (-1,-1) to (1,1)
        possible_line_directions = list(filter(lambda x: x[0] != 0 or x[1] != 0, list(product(range(-1, 2), range(-1, 2)))))

        for coord_couple in possible_line_directions:
            stack = []
            roll_needed = False
            while True:
                # Each tme we check line by line if each cell is empty or
                # full with the same color of the coin placed
                a = index_initial_cell_filled[0] + coord_couple[0]*(len(stack) + 1)
                b = index_initial_cell_filled[1] + coord_couple[1]*(len(stack) + 1)

                #If the cell doesn't exist or if it's empty we stop searching on the specific line
                if not test_cell_existence(self.board, a, b) or self.board[a][b] == 0:
                    break

                #If the cell is fill with a coin with the same color of the placed one we stop searching
                #(Following to the rules no other cells need to be rolled on the line)
                if self.board[a][b] == self.turn:
                    roll_needed = True
                    break

                stack.append((a, b))

            if roll_needed:
                sleep(self._SLEEP_TIME)
                [self.roll(index) for index in stack]

    def switch_turn(self):
        """Let the other player play
        """
        self.turn = self._PLAYER1 if self.turn == self._PLAYER2 else self._PLAYER2

    @property
    def scores(self) -> tuple:
        """Get the score of each player
        """
        return (sum([line.count(1) for line in self.board]), sum([line.count(2) for line in self.board]))

    @property
    def end_game(self) -> bool:
        """ Define whether a game is ended or not
            By returning if all the numbers are equal to 0
        """
        return all((all(row) for row in self.board))

    def roll(self, cell_index: tuple):
        """Roll a cell to the color of the other player
        """
        i, j = cell_index
        cell_pos = self.ui_settings.pos_from_cell_index((j, i))

        #Place the correspoding colored coin
        self.ui_settings.add_coin_img(self.ui_settings.red_coin, cell_pos) \
                if self.turn == self._PLAYER1 else self.ui_settings.add_coin_img(self.ui_settings.green_coin, cell_pos)
        self.board[cell_index[0]][cell_index[1]] = self.turn
        sleep(self._SLEEP_TIME)
