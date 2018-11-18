def main():
    from board_game.states.gomoku_state import GomokuState
    from .gomoku_policynet import GomokuPolicyNetModel
    from .gomoku_evaluationnet import GomokuEvaluationNetModel
    from . import policynet_train

    print('train Gomoku policynet model')

    board_shape = (9, 9)
    target = 5
    print('board_shape:', board_shape)
    print('target:', target)

    state = GomokuState(board_shape = board_shape, target = target)
    pmodel_path = 'gomoku_policynet_model_{0}_{1}_{2}'.format(board_shape[0], board_shape[1], target)
    pmodel = GomokuPolicyNetModel(board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = pmodel_path)
    emodel_path = 'gomoku_evaluationnet_model_{0}_{1}_{2}'.format(board_shape[0], board_shape[1], target)
    emodel = GomokuEvaluationNetModel(board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = emodel_path)

    config = {
        'pmodel_path' : pmodel_path,
        'emodel_path' : emodel_path,
        'discount' : 0.95,
        'batch_size' : 4,
        'learning_rate' : 0.0003,
        'episode_num' : 2000000,
    }

    policynet_train.main(state, pmodel, emodel, config)

