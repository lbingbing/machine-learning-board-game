from .policyvaluenetmcts_player import PolicyValueNetMctsPlayer
from .chess_policyvaluenet import ChessPolicyValueNetModel

class ChessPolicyValueNetMctsPlayer(PolicyValueNetMctsPlayer):
    def create_model(self, board_shape, action_dim, model_path):
        return ChessPolicyValueNetModel(board_shape = board_shape, action_dim = action_dim, model_path = model_path)

