import tkinter as tk
import tkinter.ttk
import queue
import threading
import time

from board_game.players.player import is_human

COMPUTER_STEP_DELAY_IN_SECOND = 0.5
ASYNC_RESPONSE_POLL_INTERVAL_IN_MILLISECOND = 100

class BaseApp:

    def __init__(self, player_types):
        self.init_async_worker()

        self.init_state()
        self.init_players(player_types)
        self.create_gui()
        self.bind_events()
        self.reset()

    def init_async_worker(self):
        self.request_queue = queue.Queue()
        self.response_queue = queue.Queue()

        self.worker_thread = threading.Thread(target = self.async_get_action)

        self.is_polling_async_response = False
        self.is_async_request_sent = False
        self.get_async_action_id = None

    def async_get_action(self):
        while True:
            item = self.request_queue.get()
            if item == None:
                break
            func, arg = item
            action = func(arg)
            time.sleep(COMPUTER_STEP_DELAY_IN_SECOND)
            self.response_queue.put(action)

    def mainloop(self):
        self.worker_thread.start()
        self.root.mainloop()
        self.request_queue.put(None)
        self.worker_thread.join()

    def init_state(self):
        pass

    def init_players(self, player_types):
        self.players = [self.create_player(self.state, player_type, player_id) for player_id, player_type in enumerate(player_types, 1)]

    def create_player(self, state, player_type, player_id):
        pass

    def create_gui(self):
        self.root = tk.Tk()

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
        self.redraw_pieces()
        self.reset_marker()
        self.cur_player_index = 0
        self.cur_player = self.players[self.cur_player_index]

    def cancel_async_request(self):
        if self.is_polling_async_response:
            self.root.after_cancel(self.get_async_action_id)
            self.is_polling_async_response = False
        if self.is_async_request_sent:
            self.response_queue.get()
            self.is_async_request_sent = False

    def redraw_pieces(self):
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
        return not is_human(self.cur_player)

    def computer_step(self):
        self.send_async_request()
        self.poll_async_response()

    def send_async_request(self):
        self.request_queue.put((self.cur_player.get_action, self.state))
        self.is_async_request_sent = True

    def poll_async_response(self):
        self.is_polling_async_response = False
        try:
            action = self.response_queue.get(block = False)
            self.is_async_request_sent = False
            self.apply_action(action)
            self.draw_marker(action)
            if self.is_computer_trun() and not self.state.is_end():
                self.computer_step()
        except queue.Empty:
            self.get_async_action_id = self.root.after(ASYNC_RESPONSE_POLL_INTERVAL_IN_MILLISECOND, self.poll_async_response)
            self.is_polling_async_response = True

    def handle_human_action(self, x, y):
        pass

    def get_board_position(self, x, y):
        if x < self.unit_size / 2 or \
           y < self.unit_size / 2 or \
           x > self.unit_size * (self.state.board_shape[1] + 1) - self.unit_size / 2 or \
           y > self.unit_size * (self.state.board_shape[0] + 1) - self.unit_size / 2:
            return None
        j = int(x / self.unit_size - 0.5)
        i = int(y / self.unit_size - 0.5)
        return i, j

    def apply_action(self, action):
        self.state.do_action(self.cur_player.player_id, action)

        self.redraw_pieces()
        self.root.update_idletasks()

        result = self.state.get_result()
        if result > 0:
            print('player {0} ({1}) wins'.format(result, self.cur_player.type))
        elif result == 0:
            print('draw')
        else:
            self.toggle_next_player()

    def get_piece_coord(self, position):
        x0 = (position[1] + 0.5) * self.unit_size
        y0 = (position[0] + 0.5) * self.unit_size
        x1 = x0 + self.unit_size
        y1 = y0 + self.unit_size
        return x0, y0, x1, y1

    def draw_marker(self, action):
        pass

