import tkinter as tk
import tkinter.ttk

from . import chess_state

class App:
    def __init__(self, root):
        board_height = chess_state.BOARD_HEIGHT
        board_width = chess_state.BOARD_WIDTH

        self.unit_size = 50

        canvas_width = (board_width + 1) * self.unit_size
        canvas_height = (board_height + 1) * self.unit_size

        root.resizable(width=False, height=False)
        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        frame = tk.ttk.Frame(root, borderwidth=1, relief=tk.GROOVE, padding=1)
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)
        frame.grid(row=0, column=0, padx=3, pady=3, sticky=tk.N+tk.S+tk.W+tk.E)

        self.canvas = tk.Canvas(frame, width = canvas_width, height = canvas_height)
        self.canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
        for i in range(1, board_height+1):
            x0 = self.unit_size
            x1 = board_width * self.unit_size
            y = i * self.unit_size
            self.canvas.create_line(x0, y, x1, y)
        for j in range(1, board_width+1):
            if j == 1 or j == board_width:
                x = j * self.unit_size
                y0 = self.unit_size
                y1 = board_height * self.unit_size
                self.canvas.create_line(x, y0, x, y1)
            else:
                x = j * self.unit_size
                y0 = self.unit_size
                y1 = 5 * self.unit_size
                self.canvas.create_line(x, y0, x, y1)
                y0 = 6 * self.unit_size
                y1 = board_height * self.unit_size
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
        self.canvas.create_rectangle(0, 0, 0, 0, width = 2, outline = '#ff0000', dash = (2, 2), tags = 'equivalent_src_marker')
        self.canvas.create_rectangle(0, 0, 0, 0, width = 2, outline = '#00ff00', tags = 'dst_marker')
        self.canvas.create_rectangle(0, 0, 0, 0, width = 2, outline = '#00ff00', dash = (2, 2), tags = 'equivalent_dst_marker')

        self.all_actions = []
        for action, action_index in chess_state.action_to_action_index_table.items():
            equivalent_action_index = chess_state.action_index_to_equivalent_action_index_table[action_index]
            equivalent_action = chess_state.action_index_to_action_table[equivalent_action_index]
            self.all_actions.append((action_index, action, equivalent_action_index, equivalent_action))
        self.all_actions.sort()

        self.cur_action_index = 0

        root.bind('<Left>', lambda e: self.navigate(-1))
        root.bind('<Right>', lambda e: self.navigate(1))

        self.navigate(0)

    def get_piece_coord(self, position):
        x0 = (position[1] + 0.5) * self.unit_size
        y0 = (position[0] + 0.5) * self.unit_size
        x1 = x0 + self.unit_size
        y1 = y0 + self.unit_size
        return x0, y0, x1, y1

    def navigate(self, diff):
        self.cur_action_index = (self.cur_action_index + len(self.all_actions) + diff) % len(self.all_actions)
        action = self.all_actions[self.cur_action_index][1]
        equivalent_action = self.all_actions[self.cur_action_index][3]
        coords = self.get_piece_coord((action[0], action[1]))
        self.canvas.coords('src_marker', *coords)
        coords = self.get_piece_coord((equivalent_action[0], equivalent_action[1]))
        self.canvas.coords('equivalent_src_marker', *coords)
        coords = self.get_piece_coord((action[2], action[3]))
        self.canvas.coords('dst_marker', *coords)
        coords = self.get_piece_coord((equivalent_action[2], equivalent_action[3]))
        self.canvas.coords('equivalent_dst_marker', *coords)

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

