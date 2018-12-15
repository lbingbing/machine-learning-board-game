from multiprocessing.connection import Listener
import queue
import threading
import contextlib

class TrainingMonitor:

    def __init__(self):
        self.action_queue = queue.Queue()

        self.actions = []

        self.listener = Listener(('localhost', 7777), authkey=b'machine-learning-board-game-monitor-player')
        self.connections = []

        self.lock = threading.Lock()

        self.get_connection_thread = threading.Thread(target = self.get_connection)
        self.get_connection_thread.start()

        self.broadcast_thread = threading.Thread(target = self.broadcast)
        self.broadcast_thread.start()

    def send_action(self, item):
        self.action_queue.put(item)

    def get_connection(self):
        while True:
            try:
                conn = self.listener.accept()
            except OSError:
                break
            with contextlib.suppress(ConnectionError):
                with self.lock:
                    for player_id, action in self.actions:
                        conn.send((player_id, action))
                    self.connections.append(conn)

    def broadcast(self):
        while True:
            item = self.action_queue.get()
            if item == None:
                break
            player_id, action, is_end = item
            with self.lock:
                if is_end:
                    self.actions = []
                else:
                    self.actions.append((player_id, action))
                if self.connections:
                    disconnected_conns = []
                    for conn in self.connections:
                        try:
                            conn.send((player_id, action))
                        except ConnectionError:
                            disconnected_conns.append(conn)
                    for conn in disconnected_conns:
                        self.connections.remove(conn)

    def close(self):
        self.listener.close()
        self.get_connection_thread.join()

        self.send_action(None)
        self.broadcast_thread.join()

@contextlib.contextmanager
def TrainingMonitorContext(is_training_monitor_on):
    if is_training_monitor_on:
        training_monitor = TrainingMonitor()
        try:
            yield training_monitor
        finally:
            training_monitor.close()
    else:
        yield None

