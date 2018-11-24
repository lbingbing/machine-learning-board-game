import tkinter as tk

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

def main():
    player_types = player.parse_cmd_player_types()
    app = OthelloApp(player_types)
    app.mainloop()

