from .dqn_player import DqnPlayer
from .othello_dqn import OthelloDqnModel

class OthelloDqnPlayer(DqnPlayer):
    def create_model(self, board_shape, action_dim, model_path):
        return OthelloDqnModel(board_shape = board_shape, action_dim = action_dim, model_path = model_path)

