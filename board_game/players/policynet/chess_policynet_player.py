from .policynet_player import PolicyNetPlayer
from .chess_policynet import ChessPolicyNetModel

class ChessPolicyNetPlayer(PolicyNetPlayer):
    def create_model(self, board_shape, action_dim, model_path):
        return ChessPolicyNetModel(board_shape = board_shape, action_dim = action_dim, model_path = model_path)

