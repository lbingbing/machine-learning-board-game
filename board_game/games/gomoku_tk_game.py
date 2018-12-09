import tkinter as tk
import os

from .blackwhite_tk_game import BlackWhiteApp
from board_game.states.gomoku_state import GomokuState

class GomokuApp(BlackWhiteApp):

    def init_state(self):
        board_shape = (9, 9)
        target = 5
        self.state = GomokuState(board_shape = board_shape, target = target)

    def create_player(self, state, player_type, player_id):
        from board_game.players.gomoku_player import create_player
        return create_player(state, player_type, player_id)

    def get_transcript_save_path(self):
        return os.path.join(os.path.dirname(__file__), 'gomoku.trans')

def main():
    from .utils import get_cmd_options

    args = get_cmd_options('gomoku tk game')
    player_types = (args.player_type1, args.player_type2)
    app = GomokuApp(player_types, args.save_transcript)
    app.mainloop()

