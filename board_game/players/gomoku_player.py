import os

from . import player

def create_player(state, player_type, player_id):
    p = None
    if player_type == player.HUMAN_PLAYER:
        from .human.human_player import HumanPlayer
        p = HumanPlayer(player_id = player_id)
    elif player_type == player.RANDOM_PLAYER:
        from .random.random_player import RandomPlayer
        p = RandomPlayer(player_id = player_id)
    elif player_type == player.MCTS_PLAYER:
        from .mcts.mcts_player import MctsPlayer
        p = MctsPlayer(player_id = player_id, sim_num = 5000)
    elif player_type == player.PARALLELMCTS_PLAYER:
        from .mcts.parallelmcts_player import ParallelMctsPlayer
        p = ParallelMctsPlayer(player_id = player_id, sim_num = 5000)
    elif player_type == player.CPP_MCTS_PLAYER:
        from .mcts.gomoku_cpp_mcts_player import GomokuCppMctsPlayer
        p = GomokuCppMctsPlayer(player_id = player_id, sim_num = 100000)
    elif player_type == player.DQN_PLAYER:
        from .dqn.gomoku_dqn_player import GomokuDqnPlayer
        model_path = 'gomoku_dqn_model_{0}_{1}_{2}'.format(state.board_shape[0], state.board_shape[1], state.target)
        model_path = os.path.join(os.path.dirname(__file__), 'dqn', model_path)
        p = GomokuDqnPlayer(player_id = player_id, board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = model_path)
    elif player_type == player.POLICYNET_PLAYER:
        from .policynet.gomoku_policynet_player import GomokuPolicyNetPlayer
        model_path = 'gomoku_policynet_model_{0}_{1}_{2}'.format(state.board_shape[0], state.board_shape[1], state.target)
        model_path = os.path.join(os.path.dirname(__file__), 'policynet', model_path)
        p = GomokuPolicyNetPlayer(player_id = player_id, board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = model_path)
    elif player_type == player.POLICYVALUENETMCTS_PLAYER:
        from .policyvaluenetmcts.gomoku_policyvaluenetmcts_player import GomokuPolicyValueNetMctsPlayer
        model_path = 'gomoku_policyvaluenet_model_{0}_{1}_{2}'.format(state.board_shape[0], state.board_shape[1], state.target)
        model_path = os.path.join(os.path.dirname(__file__), 'policyvaluenetmcts', model_path)
        p = GomokuPolicyValueNetMctsPlayer(player_id = player_id, board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = model_path, sim_num = 1000)
    return p

