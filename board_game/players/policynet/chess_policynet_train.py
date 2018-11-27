def main():
    import os

    from board_game.states.chess_state import ChessState
    from .chess_policynet import ChessPolicyNetModel
    from .chess_evaluationnet import ChessEvaluationNetModel
    from . import policynet_train

    print('train Chess policynet model')

    state = ChessState()
    pmodel_path = 'chess_policynet_model'
    pmodel_path = os.path.join(os.path.dirname(__file__), pmodel_path)
    pmodel = ChessPolicyNetModel(board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = pmodel_path)
    emodel_path = 'chess_evaluationnet_model'
    emodel_path = os.path.join(os.path.dirname(__file__), emodel_path)
    emodel = ChessEvaluationNetModel(board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = emodel_path)

    config = {
        'pmodel_path' : pmodel_path,
        'emodel_path' : emodel_path,
        'discount' : 0.95,
        'batch_size' : 4,
        'learning_rate' : 0.0003,
        'episode_num' : 2000000,
        'save_flag_file_path' : os.path.join(os.path.dirname(__file__), 'chess_policynet_train.save'),
        'saved_flag_file_path' : os.path.join(os.path.dirname(__file__), 'chess_policynet_train.saved'),
        'stop_flag_file_path' : os.path.join(os.path.dirname(__file__), 'chess_policynet_train.stop'),
    }

    policynet_train.main(state, pmodel, emodel, config)

