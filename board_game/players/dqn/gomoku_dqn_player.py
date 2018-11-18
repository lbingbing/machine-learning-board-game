from .dqn_player import DqnPlayer
from .gomoku_dqn import GomokuDqnModel

class GomokuDqnPlayer(DqnPlayer):
    def create_model(self, board_shape, action_dim, model_path):
        return GomokuDqnModel(board_shape = board_shape, action_dim = action_dim, model_path = model_path)

