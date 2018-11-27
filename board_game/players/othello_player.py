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
        p = MctsPlayer(player_id = player_id, sim_num = 500)
    elif player_type == player.PARALLELMCTS_PLAYER:
        from .mcts.parallelmcts_player import ParallelMctsPlayer
        p = ParallelMctsPlayer(player_id = player_id, sim_num = 500)
    elif player_type == player.CPP_MCTS_PLAYER:
        from .mcts.othello_cpp_mcts_player import OthelloCppMctsPlayer
        p = OthelloCppMctsPlayer(player_id = player_id, sim_num = 10000)
    elif player_type == player.DQN_PLAYER:
        from .dqn.othello_dqn_player import OthelloDqnPlayer
        model_path = 'othello_dqn_model_{0}_{1}'.format(state.board_shape[0], state.board_shape[1])
        model_path = os.path.join(os.path.dirname(__file__), 'dqn', model_path)
        p = OthelloDqnPlayer(player_id = player_id, board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = model_path)
    elif player_type == player.POLICYNET_PLAYER:
        from .policynet.othello_policynet_player import OthelloPolicyNetPlayer
        model_path = 'othello_policynet_model_{0}_{1}'.format(state.board_shape[0], state.board_shape[1])
        model_path = os.path.join(os.path.dirname(__file__), 'policynet', model_path)
        p = OthelloPolicyNetPlayer(player_id = player_id, board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = model_path)
    elif player_type == player.POLICYVALUENETMCTS_PLAYER:
        from .policyvaluenetmcts.othello_policyvaluenetmcts_player import OthelloPolicyValueNetMctsPlayer
        model_path = 'othello_policyvaluenet_model_{0}_{1}'.format(state.board_shape[0], state.board_shape[1])
        model_path = os.path.join(os.path.dirname(__file__), 'policyvaluenetmcts', model_path)
        p = OthelloPolicyValueNetMctsPlayer(player_id = player_id, board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = model_path, sim_num = 1000)
    return p

