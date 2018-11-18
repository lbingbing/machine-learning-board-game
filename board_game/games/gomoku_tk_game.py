import tkinter as tk

from .tk_game import BaseApp
from board_game.states.gomoku_state import GomokuState
from board_game.players import player

class GomokuApp(BaseApp):

    def init_state(self):
        board_shape = (9, 9)
        target = 5
        self.state = GomokuState(board_shape = board_shape, target = target)

    def create_player(self, state, player_type, player_id):
        from board_game.players.gomoku_player import create_player
        return create_player(state, player_type, player_id)

    def create_board(self):
        self.unit_size = 50
        canvas_height = (self.state.board_shape[0] + 1) * self.unit_size
        canvas_width = (self.state.board_shape[1] + 1) * self.unit_size
        self.canvas = tk.Canvas(self.frame, width = canvas_width, height = canvas_height)
        self.canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
        for i in range(1, self.state.board_shape[0]+1):
            x0 = self.unit_size
            x1 = self.state.board_shape[1] * self.unit_size
            y = i * self.unit_size
            self.canvas.create_line(x0, y, x1, y)
        for j in range(1, self.state.board_shape[1]+1):
            x = j * self.unit_size
            y0 = self.unit_size
            y1 = self.state.board_shape[0] * self.unit_size
            self.canvas.create_line(x, y0, x, y1)
        self.canvas.create_rectangle(0, 0, 0, 0, width = 2, outline = '#00ff00', tags = 'marker')

    def reset_pieces(self):
        self.canvas.delete('pieces')

    def reset_marker(self):
        self.canvas.coords('marker', 0, 0, 0, 0)

    def handle_human_action(self, x, y):
        if not self.is_computer_trun() and not self.state.is_end():
            action = self.get_board_position(x, y)
            if action != None and action in self.state.get_legal_actions(self.cur_player.player_id):
                self.apply_action(action)
                self.draw_marker(action)
                if self.is_computer_trun() and not self.state.is_end():
                    self.computer_step()

    def draw_action(self, action):
        coords = self.get_piece_coord(action)
        piece_color = '#000000' if self.cur_player.player_id == 1 else '#ffffff'
        self.canvas.create_oval(*coords, fill = piece_color, tags = 'pieces')

    def draw_marker(self, action):
        coords = self.get_piece_coord(action)
        self.canvas.coords('marker', *coords)
        self.canvas.tag_raise('marker', 'pieces')

def main():
    player_types = player.parse_cmd_player_types()
    app = GomokuApp(player_types)
    app.mainloop()

