import random
import concurrent.futures
import subprocess

import mcts
import parallelmcts
import dqn
import policynet
import policyvaluenet
import policyvaluenetmcts

class Player:
    def __init__(self, player_id):
        self.player_id = player_id

    def get_action(self, state):
        assert(state.get_cur_player_id()==self.player_id)

class RandomPlayer(Player):
    name = 'random'
    ishuman = False

    def get_action(self, state):
        super().get_action(state)
        return random.choice(state.get_legal_actions(self.player_id))

class MctsPlayer(Player):
    name = 'mcts'
    ishuman = False

    def __init__(self, player_id, sim_num):
        super().__init__(player_id)

        self.sim_num = sim_num

    def get_action(self, state):
        super().get_action(state)
        mcts_tree = mcts.MctsTree(root_state = state, player_id = self.player_id, sim_num = self.sim_num)
        return mcts_tree.get_action(state, self.player_id)

class ParallelMctsPlayer(Player):
    name = 'parallelmcts'
    ishuman = False

    def __init__(self, player_id, sim_num):
        super().__init__(player_id)

        self.sim_num = sim_num
        self.executor = concurrent.futures.ProcessPoolExecutor()

    def get_action(self, state):
        super().get_action(state)
        mcts_tree = parallelmcts.MctsTree(executor = self.executor, root_state = state, player_id = self.player_id, sim_num = self.sim_num)
        return mcts_tree.get_action(state, self.player_id)

class CppMctsPlayer(Player):
    name = 'cppmcts'
    ishuman = False

    def __init__(self, player_id, sim_num):
        super().__init__(player_id)

        self.sim_num = sim_num

    def get_action(self, state):
        super().get_action(state)
        res = subprocess.run(state.cmd_strs() + [str(self.sim_num)], stdout = subprocess.PIPE, check = True, encoding = 'utf-8')
        action = tuple(map(int, res.stdout.strip()[1:-1].split(', ')))
        return action

class DqnPlayer(Player):
    name = 'dqn'
    ishuman = False

    def __init__(self, player_id, board_shape, action_dim, model_name):
        super().__init__(player_id)

        self.model = dqn.DqnModel(board_shape = board_shape, action_dim = action_dim, model_name = model_name)
        self.model.load()

    def get_action(self, state):
        super().get_action(state)
        return dqn.get_opt_action(self.model, state)

class PolicyNetPlayer(Player):
    name = 'policynet'
    ishuman = False

    def __init__(self, player_id, board_shape, action_dim, model_name):
        super().__init__(player_id)

        self.model = policynet.PolicyNetModel(board_shape = board_shape, action_dim = action_dim, model_name = model_name)
        self.model.load()

    def get_action(self, state):
        super().get_action(state)
        return policynet.get_action(self.model, state, self.player_id)

class PolicyValueNetMctsPlayer(Player):
    name = 'policyvaluenetmcts'
    ishuman = False

    def __init__(self, player_id, board_shape, action_dim, model_name, sim_num):
        super().__init__(player_id)

        self.model = policyvaluenet.PolicyValueNetModel(board_shape = board_shape, action_dim = action_dim, model_name = model_name)
        self.model.load()
        self.sim_num = sim_num

    def get_action(self, state):
        super().get_action(state)
        mcts_tree = policyvaluenetmcts.MctsTree(model = self.model, root_state = state, player_id = self.player_id, sim_num = self.sim_num, self_play = False)
        action, Ps_m = mcts_tree.get_action(state, self.player_id)
        return action

class HumanPlayer(Player):
    name = 'human'
    ishuman = True

    def get_action(self, state):
        super().get_action(state)
        # input action in format 'x,y'
        while True:
            action_str = input()
            try:
                action = action_str.split(',')
                if len(action) != 2:
                    raise ValueError
                action = tuple(map(int, action))
                if action not in state.get_legal_actions(self.player_id):
                    raise ValueError
                break
            except ValueError:
                print("illegal action '{0}'".format(action_str))
        return action

