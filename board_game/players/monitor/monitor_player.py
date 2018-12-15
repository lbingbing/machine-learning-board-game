from multiprocessing.connection import Client
import time

from board_game.players import player

class MonitorPlayer(player.Player):
    type = player.MONITOR_PLAYER

    def __init__(self, player_id):
        super().__init__(player_id)

        while True:
            try:
                self.conn = Client(('localhost', 7777), authkey=b'machine-learning-board-game-monitor-player')
                break
            except ConnectionError:
                time.sleep(1)

    def get_action(self, state):
        while True:
            player_id, action = self.conn.recv()
            if player_id == self.player_id:
                break
        assert(action in state.get_legal_actions(self.player_id))
        return action

