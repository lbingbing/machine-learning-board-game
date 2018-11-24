from .policynet_player import PolicyNetPlayer
from .othello_policynet import OthelloPolicyNetModel

class OthelloPolicyNetPlayer(PolicyNetPlayer):
    def create_model(self, board_shape, action_dim, model_path):
        return OthelloPolicyNetModel(board_shape = board_shape, action_dim = action_dim, model_path = model_path)

