from board_game.players import player
from .mcts import MctsTree

class MctsPlayer(player.Player):
    type = player.MCTS_PLAYER

    def __init__(self, player_id, sim_num):
        super().__init__(player_id)

        self.sim_num = sim_num

    def get_action(self, state):
        super().get_action(state)
        mcts_tree = MctsTree(root_state = state, player_id = self.player_id, sim_num = self.sim_num)
        return mcts_tree.get_action(state, self.player_id)

