def main():
    from board_game.states.chess_state import ChessState
    from .chess_dqn import ChessDqnModel
    from . import dqn_train

    print('train Chess dqn model')

    state = ChessState()
    model_path = 'chess_dqn_model'
    model = ChessDqnModel(board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = model_path)

    config = {
        'model_path' : model_path,
        'replaymemory_file_path' : 'chess_dqn_replaymemory.pickle',
        'replaymemory_size' : 64 * 1024,
        'discount' : 0.95,
        'batch_size' : 16,
        'epoch_num' : 4,
        'learning_rate' : 0.001,
        'episode_num' : 2000000,
    }

    dqn_train.main(state, model, config)

