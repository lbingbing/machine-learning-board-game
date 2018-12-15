def get_config():
    import os

    from board_game.states.othello_state import OthelloState
    from .othello_policyvaluenet import OthelloPolicyValueNetModel

    board_shape = (8, 8)
    print('board_shape:', board_shape)

    state = OthelloState(board_shape = board_shape)
    model_path = 'othello_policyvaluenet_model_{0}_{1}'.format(board_shape[0], board_shape[1])
    model_path = os.path.join(os.path.dirname(__file__), model_path)
    model = OthelloPolicyValueNetModel(board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = model_path)

    config = {
        'model_path' : model_path,
        'replay_memory_size' : 64 * 1024,
        'sim_num' : 1000,
        'dirichlet_factor' : 0.25,
        'dirichlet_alpha' : 0.03,
        'epoch_num' : 16,
        'batch_size' : 128,
        'learning_rate' : 0.003,
        'episode_num' : 2000000,
    }

    return state, model, config

def main():
    from . import policyvaluenet_train

    policyvaluenet_train.main('othello', get_config)

