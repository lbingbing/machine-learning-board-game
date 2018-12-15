def get_config():
    import os

    from board_game.states.chess_state import ChessState
    from .chess_dqn import ChessDqnModel

    state = ChessState()
    model_path = 'chess_dqn_model'
    model_path = os.path.join(os.path.dirname(__file__), model_path)
    model = ChessDqnModel(board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = model_path)

    config = {
        'model_path' : model_path,
        'replay_memory_size' : 64 * 1024,
        'discount' : 0.95,
        'batch_size' : 16,
        'epoch_num' : 4,
        'learning_rate' : 0.001,
        'episode_num' : 2000000,
    }

    return state, model, config

def main():
    from . import dqn_train

    dqn_train.main('chess', get_config)

