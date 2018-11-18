HUMAN_PLAYER              = 'human'
RANDOM_PLAYER             = 'random'
MCTS_PLAYER               = 'mcts'
PARALLELMCTS_PLAYER       = 'parallelmcts'
CPP_MCTS_PLAYER           = 'cpp_mcts'
DQN_PLAYER                = 'dqn'
POLICYNET_PLAYER          = 'policynet'
POLICYVALUENETMCTS_PLAYER = 'policyvaluenetmcts'

PLAYER_TYPES = [
                HUMAN_PLAYER,
                RANDOM_PLAYER,
                MCTS_PLAYER,
                PARALLELMCTS_PLAYER,
                CPP_MCTS_PLAYER,
                DQN_PLAYER,
                POLICYNET_PLAYER,
                POLICYVALUENETMCTS_PLAYER,
               ]

class Player:
    type = None

    def __init__(self, player_id):
        self.player_id = player_id

    def get_action(self, state):
        assert(state.get_cur_player_id()==self.player_id)

def is_human(player):
    return player.type == HUMAN_PLAYER

def parse_cmd_player_types():
    import argparse

    parser = argparse.ArgumentParser(description='player type')
    parser.add_argument('p1', choices=PLAYER_TYPES, help='player1 type')
    parser.add_argument('p2', choices=PLAYER_TYPES, help='player2 type')
    args = parser.parse_args()

    return args.p1, args.p2

