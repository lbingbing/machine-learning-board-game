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
        from .mcts.chess_cpp_mcts_player import ChessCppMctsPlayer
        p = ChessCppMctsPlayer(player_id = player_id, sim_num = 100000)
    elif player_type == player.DQN_PLAYER:
        from .dqn.chess_dqn_player import ChessDqnPlayer
        model_path = os.path.join(os.path.dirname(__file__), 'dqn', 'chess_dqn_model')
        p = ChessDqnPlayer(player_id = player_id, board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = model_path)
    elif player_type == player.POLICYNET_PLAYER:
        from .policynet.chess_policynet_player import ChessPolicyNetPlayer
        model_path = os.path.join(os.path.dirname(__file__), 'policynet', 'chess_policynet_model')
        p = ChessPolicyNetPlayer(player_id = player_id, board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = model_path)
    elif player_type == player.POLICYVALUENETMCTS_PLAYER:
        from .policyvaluenetmcts.chess_policyvaluenetmcts_player import ChessPolicyValueNetMctsPlayer
        model_path = os.path.join(os.path.dirname(__file__), 'policyvaluenetmcts', 'chess_policyvaluenet_model')
        p = ChessPolicyValueNetMctsPlayer(player_id = player_id, board_shape = state.board_shape, action_dim = state.get_action_dim(), model_path = model_path, sim_num = 1000)
    return p

