import concurrent.futures

from board_game.players import player
from .parallelmcts import MctsTree

class ParallelMctsPlayer(player.Player):
    type = player.PARALLELMCTS_PLAYER

    def __init__(self, player_id, sim_num):
        super().__init__(player_id)

        self.sim_num = sim_num
        self.executor = concurrent.futures.ProcessPoolExecutor()

    def get_action(self, state):
        super().get_action(state)
        mcts_tree = MctsTree(executor = self.executor, root_state = state, player_id = self.player_id, sim_num = self.sim_num)
        return mcts_tree.get_action(state, self.player_id)

