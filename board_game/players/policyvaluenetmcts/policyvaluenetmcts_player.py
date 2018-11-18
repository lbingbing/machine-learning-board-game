from board_game.players import player
from .policyvaluenetmcts import MctsTree

class PolicyValueNetMctsPlayer(player.Player):
    type = player.POLICYVALUENETMCTS_PLAYER

    def __init__(self, player_id, board_shape, action_dim, model_path, sim_num):
        super().__init__(player_id)

        self.model = self.create_model(board_shape = board_shape, action_dim = action_dim, model_path = model_path)
        self.model.load()
        self.sim_num = sim_num

    def create_model(self, board_shape, action_dim, model_path):
        pass

    def get_action(self, state):
        super().get_action(state)
        mcts_tree = MctsTree(model = self.model, root_state = state, player_id = self.player_id, sim_num = self.sim_num, is_training = False)
        action, Ps_m = mcts_tree.get_action(state, self.player_id)
        return action

