from .policyvaluenetmcts_player import PolicyValueNetMctsPlayer
from .gomoku_policyvaluenet import GomokuPolicyValueNetModel

class GomokuPolicyValueNetMctsPlayer(PolicyValueNetMctsPlayer):
    def create_model(self, board_shape, action_dim, model_path):
        return GomokuPolicyValueNetModel(board_shape = board_shape, action_dim = action_dim, model_path = model_path)

