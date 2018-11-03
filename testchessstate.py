import tkinter as tk
import tkinter.ttk

import chessstate

root = tk.Tk()

state = chessstate.ChessState()
unit_size = 50
canvas_width = (state.board_shape[1] + 1) * unit_size
canvas_height = (state.board_shape[0] + 1) * unit_size

root.resizable(width=False, height=False)
root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

frame = tk.ttk.Frame(root, borderwidth=1, relief=tk.GROOVE, padding=1)
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
frame.grid(row=0, column=0, padx=3, pady=3, sticky=tk.N+tk.S+tk.W+tk.E)

canvas = tk.Canvas(frame, width = canvas_width, height = canvas_height)
canvas.grid(row=0, column=0, sticky=tk.N+tk.S+tk.W+tk.E)
for i in range(1, state.board_shape[0]+1):
    x0 = unit_size
    x1 = state.board_shape[1] * unit_size
    y = i * unit_size
    canvas.create_line(x0, y, x1, y)
for j in range(1, state.board_shape[1]+1):
    if j == 1 or j == state.board_shape[1]:
        x = j * unit_size
        y0 = unit_size
        y1 = state.board_shape[0] * unit_size
        canvas.create_line(x, y0, x, y1)
    else:
        x = j * unit_size
        y0 = unit_size
        y1 = 5 * unit_size
        canvas.create_line(x, y0, x, y1)
        y0 = 6 * unit_size
        y1 = state.board_shape[0] * unit_size
        canvas.create_line(x, y0, x, y1)
coords = (4 * unit_size,
          unit_size,
          6 * unit_size,
          3 * unit_size)
canvas.create_line(*coords)
coords = (4 * unit_size,
          3 * unit_size,
          6 * unit_size,
          1 * unit_size)
canvas.create_line(*coords)
coords = (4 * unit_size,
          8 * unit_size,
          6 * unit_size,
          10 * unit_size)
canvas.create_line(*coords)
coords = (4 * unit_size,
          10 * unit_size,
          6 * unit_size,
          8 * unit_size)
canvas.create_line(*coords)
canvas.create_rectangle(0, 0, 0, 0, width = 2, outline = '#ff0000', tags = 'src_marker')
canvas.create_rectangle(0, 0, 0, 0, width = 2, outline = '#ff0000', dash = (2, 2), tags = 'equivalent_src_marker')
canvas.create_rectangle(0, 0, 0, 0, width = 2, outline = '#00ff00', tags = 'dst_marker')
canvas.create_rectangle(0, 0, 0, 0, width = 2, outline = '#00ff00', dash = (2, 2), tags = 'equivalent_dst_marker')

all_actions = []
for action, action_index in chessstate.action_to_action_index_table.items():
    equivalent_action_index = chessstate.action_index_to_equivalent_action_index_table[action_index]
    equivalent_action = chessstate.action_index_to_action_table[equivalent_action_index]
    all_actions.append((action_index, action, equivalent_action_index, equivalent_action))
all_actions.sort()
cur_action_index = 0

def get_piece_coord(position):
    x0 = (position[1] + 0.5) * unit_size
    y0 = (position[0] + 0.5) * unit_size
    x1 = x0 + unit_size
    y1 = y0 + unit_size
    return x0, y0, x1, y1

def navigate(diff):
    global cur_action_index

    cur_action_index = (cur_action_index + len(all_actions) + diff) % len(all_actions)
    action = all_actions[cur_action_index][1]
    equivalent_action = all_actions[cur_action_index][3]
    coords = get_piece_coord((action[0], action[1]))
    canvas.coords('src_marker', *coords)
    coords = get_piece_coord((equivalent_action[0], equivalent_action[1]))
    canvas.coords('equivalent_src_marker', *coords)
    coords = get_piece_coord((action[2], action[3]))
    canvas.coords('dst_marker', *coords)
    coords = get_piece_coord((equivalent_action[2], equivalent_action[3]))
    canvas.coords('equivalent_dst_marker', *coords)

root.bind('<Left>', lambda e: navigate(-1))
root.bind('<Right>', lambda e: navigate(1))

navigate(0)

root.mainloop()

