from .policyvaluenetmcts_player import PolicyValueNetMctsPlayer
from .othello_policyvaluenet import OthelloPolicyValueNetModel

class OthelloPolicyValueNetMctsPlayer(PolicyValueNetMctsPlayer):
    def create_model(self, board_shape, action_dim, model_path):
        return OthelloPolicyValueNetModel(board_shape = board_shape, action_dim = action_dim, model_path = model_path)

