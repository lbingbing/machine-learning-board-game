def get_config():
    import os
    from board_game.states.gomoku_state import GomokuState
    from .gomoku_policyvaluenet import GomokuPolicyValueNetModel

    board_shape = (9, 9)
    target = 5
    print('board_shape:', board_shape)
    print('target:', target)

    state = GomokuState(board_shape = board_shape, target = target)
    model_path = 'gomoku_policyvaluenet_model_{0}_{1}_{2}'.format(board_shape[0], board_shape[1], target)
    model_path = os.path.join(os.path.dirname(__file__), model_path)
    model = GomokuPolicyValueNetModel(board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = model_path)

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

    policyvaluenet_train.main('gomoku', get_config)

