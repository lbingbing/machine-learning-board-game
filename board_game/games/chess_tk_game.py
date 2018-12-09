import tkinter as tk
import os

from .tk_game import BaseApp
from board_game.states import chess_state

class ChessApp(BaseApp):

    def init_state(self):
        self.state = chess_state.ChessState()

    def create_player(self, state, player_type, player_id):
        from board_game.players.chess_player import create_player
        return create_player(state, player_type, player_id)

    def create_board(self):
        self.unit_size = 50
        canvas_width = (self.state.board_shape[1] + 1) * self.unit_size
        canvas_height = (self.state.board_shape[0] + 1) * self.unit_size
        self.canvas = tk.Canvas(self.frame, width = canvas_width, height = canvas_height)
        self.canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
        for i in range(1, self.state.board_shape[0]+1):
            x0 = self.unit_size
            x1 = self.state.board_shape[1] * self.unit_size
            y = i * self.unit_size
            self.canvas.create_line(x0, y, x1, y)
        for j in range(1, self.state.board_shape[1]+1):
            if j == 1 or j == self.state.board_shape[1]:
                x = j * self.unit_size
                y0 = self.unit_size
                y1 = self.state.board_shape[0] * self.unit_size
                self.canvas.create_line(x, y0, x, y1)
            else:
                x = j * self.unit_size
                y0 = self.unit_size
                y1 = 5 * self.unit_size
                self.canvas.create_line(x, y0, x, y1)
                y0 = 6 * self.unit_size
                y1 = self.state.board_shape[0] * self.unit_size
                self.canvas.create_line(x, y0, x, y1)
        coords = (4 * self.unit_size,
                  self.unit_size,
                  6 * self.unit_size,
                  3 * self.unit_size)
        self.canvas.create_line(*coords)
        coords = (4 * self.unit_size,
                  3 * self.unit_size,
                  6 * self.unit_size,
                  1 * self.unit_size)
        self.canvas.create_line(*coords)
        coords = (4 * self.unit_size,
                  8 * self.unit_size,
                  6 * self.unit_size,
                  10 * self.unit_size)
        self.canvas.create_line(*coords)
        coords = (4 * self.unit_size,
                  10 * self.unit_size,
                  6 * self.unit_size,
                  8 * self.unit_size)
        self.canvas.create_line(*coords)
        self.canvas.create_rectangle(0, 0, 0, 0, width = 2, outline = '#ff0000', tags = 'src_marker')
        self.canvas.create_rectangle(0, 0, 0, 0, width = 2, outline = '#00ff00', tags = 'dst_marker')

    def reset(self):
        super().reset()

        self.human_action_src_phase = True
        self.human_action_src_position = None
        self.human_action_legal_dst_positions = None

    def redraw_pieces(self):
        self.canvas.delete('pieces')

        board = self.state.get_board()
        for i in range(self.state.board_shape[0]):
            for j in range(self.state.board_shape[1]):
                piece_value = board[i][j]
                if piece_value != chess_state.NULL:
                    coords = self.get_piece_coord((i, j))
                    piece_color = '#ff0000' if chess_state.piece_value_to_player_id(piece_value) == 1 else '#000000'
                    self.canvas.create_oval(*coords, fill = '#ffffff', outline = piece_color, tags = 'pieces')
                    piece_name = chess_state.piece_value_to_name(piece_value)
                    self.canvas.create_text((coords[0]+coords[2])/2, (coords[1]+coords[3])/2, text = piece_name, fill = piece_color, tags = 'pieces')

    def reset_marker(self):
        self.canvas.coords('src_marker', 0, 0, 0, 0)
        self.canvas.coords('dst_marker', 0, 0, 0, 0)
        self.delete_legal_dst_markers()

    def handle_human_action(self, x, y):
        if not self.is_computer_trun() and not self.state.is_end():
            position = self.get_board_position(x, y)
            if position != None:
                if self.is_self_piece(self.cur_player.player_id, position):
                    legal_dst_positions = [(action[2], action[3]) for action in self.state.get_legal_actions(self.cur_player.player_id) if (action[0], action[1]) == position]
                    self.human_action_src_phase = False
                    self.human_action_src_position = position
                    self.human_action_legal_dst_positions = legal_dst_positions
                    self.reset_marker()
                    self.draw_src_marker(position)
                    self.draw_legal_dst_markers()
                elif not self.human_action_src_phase and position in self.human_action_legal_dst_positions:
                    action = (*self.human_action_src_position, *position)
                    self.apply_action(action)
                    self.delete_legal_dst_markers()
                    self.draw_dst_marker(position)
                    self.human_action_src_phase = True
                    self.human_action_src_position = None
                    self.human_action_legal_dst_positions = None
                    if self.is_computer_trun() and not self.state.is_end():
                        self.computer_step()

    def is_self_piece(self, player_id, position):
        return chess_state.piece_value_to_player_id(self.state.get_board()[position[0]][position[1]])==player_id

    def get_transcript_save_path(self):
        return os.path.join(os.path.dirname(__file__), 'chess.trans')

    def draw_marker(self, action):
        self.draw_src_marker((action[0], action[1]))
        self.draw_dst_marker((action[2], action[3]))

    def draw_src_marker(self, position):
        coords = self.get_piece_coord(position)
        self.canvas.coords('src_marker', *coords)
        self.canvas.tag_raise('src_marker', 'pieces')

    def draw_dst_marker(self, position):
        coords = self.get_piece_coord(position)
        self.canvas.coords('dst_marker', *coords)
        self.canvas.tag_raise('dst_marker', 'pieces')

    def draw_legal_dst_markers(self):
        for dst_position in self.human_action_legal_dst_positions:
            coords = self.get_piece_coord(dst_position)
            self.canvas.create_rectangle(*coords, width = 2, outline = '#0000ff', tags = 'legal_dst_markers')

    def delete_legal_dst_markers(self):
        self.canvas.delete('legal_dst_markers')

def main():
    from .utils import get_cmd_options

    args = get_cmd_options('chess tk game')
    player_types = (args.player_type1, args.player_type2)
    app = ChessApp(player_types, args.save_transcript)
    app.mainloop()

