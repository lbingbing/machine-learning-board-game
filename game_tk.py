import tkinter as tk
import tkinter.ttk
import queue
import threading

import blackwhitestate
import chessstate

request_queue = queue.Queue()
response_queue = queue.Queue()

class BaseApp:

    def __init__(self, root, state, player1, player2):
        self.root = root

        self.computer_step_delay = 500
        self.async_response_poll_interval = 100
        self.is_polling_async_response = False
        self.is_async_request_sent = False

        self.state = state
        self.players = (player1, player2)
        self.create_gui()
        self.bind_events()
        self.reset()
        self.start()

    def create_gui(self):
        self.root.resizable(width=False, height=False)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.frame = tk.ttk.Frame(self.root, borderwidth=1, relief=tk.GROOVE, padding=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.grid(row=0, column=0, padx=3, pady=3, sticky=tk.N+tk.S+tk.W+tk.E)

        self.create_board()

    def create_board(self):
        pass

    def bind_events(self):
        self.root.bind('<Return>', lambda e: (self.reset(), self.start()))
        self.canvas.bind('<Button-1>', lambda e: self.handle_human_action(e.x, e.y))

    def reset(self):
        self.cancel_async_request()

        self.state.reset()
        self.reset_pieces()
        self.reset_marker()
        self.cur_player_index = 0
        self.cur_player = self.players[self.cur_player_index]

    def reset_pieces(self):
        pass

    def reset_marker(self):
        pass

    def start(self):
        if self.is_computer_trun():
            self.computer_step()

    def toggle_next_player(self):
        self.cur_player_index = (self.cur_player_index + 1) % 2
        self.cur_player = self.players[self.cur_player_index]

    def is_computer_trun(self):
        return not self.cur_player.ishuman

    def computer_step(self):
        self.send_async_request()
        self.poll_async_response()

    def send_async_request(self):
        request_queue.put((self.cur_player.get_action, self.state))
        self.is_async_request_sent = True

    def poll_async_response(self):
        self.is_polling_async_response = False
        try:
            action = response_queue.get(block = False)
            self.is_async_request_sent = False
            self.apply_action(action)
            self.draw_marker(action)
            if self.is_computer_trun() and not self.state.is_end():
                self.root.after(self.computer_step_delay, self.computer_step)
        except queue.Empty:
            self.get_async_action_id = self.root.after(self.async_response_poll_interval, self.poll_async_response)
            self.is_polling_async_response = True

    def cancel_async_request(self):
        if self.is_polling_async_response:
            self.root.after_cancel(self.get_async_action_id)
            self.is_polling_async_response = False
        if self.is_async_request_sent:
            response_queue.get()
            self.is_async_request_sent = False

    def handle_human_action(self, x, y):
        pass

    def apply_action(self, action):
        self.state.do_action(self.cur_player.player_id, action)

        self.draw_action(action)
        self.root.update_idletasks()

        result = self.state.get_result()
        if result >= 0:
            if result > 0:
                print('player {0} ({1}) wins'.format(result, self.cur_player.name))
            else:
                print('draw')
        else:
            self.toggle_next_player()

    def get_piece_coord(self, position):
        x0 = (position[1] + 0.5) * self.unit_size
        y0 = (position[0] + 0.5) * self.unit_size
        x1 = x0 + self.unit_size
        y1 = y0 + self.unit_size
        return x0, y0, x1, y1

    def draw_action(self, action):
        pass

    def draw_marker(self, action):
        pass

class BlackWhiteApp(BaseApp):

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

    def get_board_position(self, x, y):
        if x < self.unit_size / 2 or \
           y < self.unit_size / 2 or \
           x > self.unit_size * (self.state.board_shape[1] + 1) - self.unit_size / 2 or \
           y > self.unit_size * (self.state.board_shape[0] + 1) - self.unit_size / 2:
            return None
        j = int(x / self.unit_size - 0.5)
        i = int(y / self.unit_size - 0.5)
        return i, j

    def draw_action(self, action):
        coords = self.get_piece_coord(action)
        piece_color = '#000000' if self.cur_player.player_id == 1 else '#ffffff'
        self.canvas.create_oval(*coords, fill = piece_color, tags = 'pieces')

    def draw_marker(self, action):
        coords = self.get_piece_coord(action)
        self.canvas.coords('marker', *coords)
        self.canvas.tag_raise('marker', 'pieces')

class ChessApp(BaseApp):

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

    def reset_pieces(self):
        self.piece_canvas_objs = {}
        self.canvas.delete('pieces')

        board = self.state.get_board()
        for i in range(self.state.board_shape[0]):
            for j in range(self.state.board_shape[1]):
                piece_value = board[i][j]
                if piece_value != chessstate.NULL:
                    piece_color = '#ff0000' if chessstate.piece_value_to_player_id(piece_value) == 1 else '#000000'
                    piece_oval_canvas_obj = self.canvas.create_oval(0, 0, 0, 0, fill = '#ffffff', outline = piece_color, tags = 'pieces')
                    piece_name = chessstate.piece_value_to_name(piece_value)
                    piece_text_canvas_obj = self.canvas.create_text(0, 0, text = piece_name, fill = piece_color, tags = 'pieces')
                    piece_canvas_obj = {
                            'oval' : piece_oval_canvas_obj,
                            'text' : piece_text_canvas_obj,
                        }
                    self.place_piece(piece_canvas_obj, (i, j))

    def place_piece(self, piece_canvas_obj, position):
        assert(position not in self.piece_canvas_objs)
        self.piece_canvas_objs[position] = piece_canvas_obj

        piece_oval_canvas_obj = piece_canvas_obj['oval']
        piece_text_canvas_obj = piece_canvas_obj['text']
        coords = self.get_piece_coord(position)
        self.canvas.coords(piece_oval_canvas_obj, *coords)
        self.canvas.coords(piece_text_canvas_obj, (coords[0]+coords[2])/2, (coords[1]+coords[3])/2)

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

    def get_board_position(self, x, y):
        if x < self.unit_size / 2 or \
           y < self.unit_size / 2 or \
           x > self.unit_size * (self.state.board_shape[1] + 1) - self.unit_size / 2 or \
           y > self.unit_size * (self.state.board_shape[0] + 1) - self.unit_size / 2:
            return None
        j = int(x / self.unit_size - 0.5)
        i = int(y / self.unit_size - 0.5)
        return i, j

    def is_self_piece(self, player_id, position):
        return chessstate.piece_value_to_player_id(self.state.board[position[0]][position[1]])==player_id

    def draw_action(self, action):
        src_position = (action[0], action[1])
        dst_position = (action[2], action[3])

        dst_piece_canvas_obj = self.piece_canvas_objs.pop(dst_position, None)
        if dst_piece_canvas_obj != None:
            dst_piece_oval_canvas_obj = dst_piece_canvas_obj['oval']
            dst_piece_text_canvas_obj = dst_piece_canvas_obj['text']
            self.canvas.delete(dst_piece_oval_canvas_obj)
            self.canvas.delete(dst_piece_text_canvas_obj)

        src_piece_canvas_obj = self.piece_canvas_objs[src_position]
        del self.piece_canvas_objs[src_position]
        self.place_piece(src_piece_canvas_obj, dst_position)

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

def async_get_action():
    while True:
       item = request_queue.get()
       if item == None:
           break
       func, arg = item
       action = func(arg)
       response_queue.put(action)

def main():
    import player

    root = tk.Tk()

    game_name = 'Gomoku'
    #game_name = 'Chess'

    if game_name == 'Gomoku':
        board_shape = (9, 9)
        target = 5
        state = blackwhitestate.GomokuState(board_shape = board_shape, target = target)
        dqn_model_name = 'gomoku_dqn_model_{0}_{1}_{2}'.format(board_shape[0], board_shape[1], target)
        policynet_model_name = 'gomoku_policynet_model_{0}_{1}_{2}'.format(board_shape[0], board_shape[1], target)
        policyvaluenet_model_name = 'gomoku_policyvaluenet_model_{0}_{1}_{2}'.format(board_shape[0], board_shape[1], target)
        App = BlackWhiteApp

    elif game_name == 'Chess':
        state = chessstate.ChessState()
        dqn_model_name = 'chess_dqn_model'
        policynet_model_name = 'chess_policynet_model'
        policyvaluenet_model_name = 'chess_policyvaluenet_model'
        App = ChessApp

    #player1 = player.RandomPlayer(player_id = 1)
    #player1 = player.MctsPlayer(player_id = 1, sim_num = 5000)
    #player1 = player.CppMctsPlayer(player_id = 1, sim_num = 100000)
    #player1 = player.DqnPlayer(player_id = 1, board_shape = state.board_shape, action_dim = state.get_action_dim(), model_name = dqn_model_name)
    #player1 = player.PolicyNetPlayer(player_id = 1, board_shape = state.board_shape, action_dim = state.get_action_dim(), model_name = policynet_model_name)
    player1 = player.PolicyValueNetMctsPlayer(player_id = 1, board_shape = state.board_shape, action_dim = state.get_action_dim(), model_name = policyvaluenet_model_name, sim_num = 1000)
    #player1 = player.HumanPlayer(player_id = 1)
    #player2 = player.RandomPlayer(player_id = 2)
    #player2 = player.MctsPlayer(player_id = 2, sim_num = 5000)
    #player2 = player.CppMctsPlayer(player_id = 2, sim_num = 100000)
    #player2 = player.DqnPlayer(player_id = 2, board_shape = state.board_shape, action_dim = state.get_action_dim(), model_name = dqn_model_name)
    #player2 = player.PolicyNetPlayer(player_id = 2, board_shape = state.board_shape, action_dim = state.get_action_dim(), model_name = policynet_model_name)
    player2 = player.PolicyValueNetMctsPlayer(player_id = 2, board_shape = state.board_shape, action_dim = state.get_action_dim(), model_name = policyvaluenet_model_name, sim_num = 1000)
    #player2 = player.HumanPlayer(player_id = 2)

    app = App(root, state, player1, player2)

    worker_thread = threading.Thread(target = async_get_action)
    worker_thread.start()
    root.mainloop()
    request_queue.put(None)
    worker_thread.join()

if __name__ == '__main__':
    main()
