from .dqn_player import DqnPlayer
from .chess_dqn import ChessDqnModel

class ChessDqnPlayer(DqnPlayer):
    def create_model(self, board_shape, action_dim, model_path):
        return ChessDqnModel(board_shape = board_shape, action_dim = action_dim, model_path = model_path)

