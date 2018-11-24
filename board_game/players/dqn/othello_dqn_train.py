def main():
    from board_game.states.othello_state import OthelloState
    from .othello_dqn import OthelloDqnModel
    from . import dqn_train

    print('train Othello dqn model')

    board_shape = (8, 8)
    print('board_shape:', board_shape)

    state = OthelloState(board_shape = board_shape)
    model_path = 'othello_dqn_model_{0}_{1}'.format(board_shape[0], board_shape[1])
    model = OthelloDqnModel(board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = model_path)

    config = {
        'model_path' : model_path,
        'replaymemory_file_path' : 'othello_dqn_replaymemory.pickle',
        'replaymemory_size' : 64 * 1024,
        'discount' : 0.95,
        'batch_size' : 16,
        'epoch_num' : 4,
        'learning_rate' : 0.001,
        'episode_num' : 2000000,
    }

    dqn_train.main(state, model, config)

