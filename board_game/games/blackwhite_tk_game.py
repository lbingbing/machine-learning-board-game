import tkinter as tk

from .tk_game import BaseApp
from board_game.players import player

class BlackWhiteApp(BaseApp):

    def init_state(self):
        pass

    def create_player(self, state, player_type, player_id):
        pass

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

    def redraw_pieces(self):
        self.canvas.delete('pieces')

        board = self.state.get_board()
        for i in range(self.state.board_shape[0]):
            for j in range(self.state.board_shape[1]):
                player_id = board[i][j]
                if player_id != 0:
                    coords = self.get_piece_coord((i, j))
                    piece_color = '#000000' if player_id == 1 else '#ffffff'
                    self.canvas.create_oval(*coords, fill = piece_color, tags = 'pieces')

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

    def draw_marker(self, action):
        coords = self.get_piece_coord(action)
        self.canvas.coords('marker', *coords)
        self.canvas.tag_raise('marker', 'pieces')

