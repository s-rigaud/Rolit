"""Main executable file"""

from rolit_game.game import Game
from rolit_game.popup import Popup

game = Game()
game_config = Popup.game_config()
board_size, gamemode, ai_level, user_wants_game = game_config.split('  ')
board_size = int(board_size.split('x')[0])
user_wants_game = user_wants_game == 'True'

#If the user doesn't close the config panel before clicking "Let's play !"
if user_wants_game:
    game.config(board_size, gamemode, ai_level)
    game.play()

