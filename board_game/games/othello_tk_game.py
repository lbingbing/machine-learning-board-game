import tkinter as tk
import os

from .blackwhite_tk_game import BlackWhiteApp
from board_game.states.othello_state import OthelloState
from board_game.players import player

class OthelloApp(BlackWhiteApp):

    def init_state(self):
        board_shape = (8, 8)
        self.state = OthelloState(board_shape = board_shape)

    def create_player(self, state, player_type, player_id):
        from board_game.players.othello_player import create_player
        return create_player(state, player_type, player_id)

    def get_transcript_save_path(self):
        return os.path.join(os.path.dirname(__file__), 'othello.trans')

def main():
    from .utils import get_cmd_options

    args = get_cmd_options('othello tk game')
    player_types = (args.player_type1, args.player_type2)
    app = OthelloApp(player_types, args.save_transcript)
    app.mainloop()

