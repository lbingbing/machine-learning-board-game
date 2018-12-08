import random
import math
import copy
import numpy as np
import graphviz

from board_game.utils.utils import get_next_player_id

class Node:
    def __init__(self, player_id = None, action = None, P = None, parent = None):
        self.player_id = player_id # player_id that takes the action
        self.action = action # the action that player takes
        self.N = 0
        self.W = 0
        self.Q = 0
        self.P = P

        self.children = []
        self.parent = parent

    def __str__(self):
        return 'player_id={0}\naction={1}\nN={2}\nW={3}\nQ={4}\nP={5}'.format(self.player_id, self.action, self.N, self.W, self.Q, self.P)

    def is_leaf(self):
        return not bool(self.children)

    def get_uct_value(self):
        return self.get_uct_value_exploitation_factor() + self.get_uct_value_exploration_factor()

    def get_uct_value_exploitation_factor(self):
        return self.Q

    def get_uct_value_exploration_factor(self):
        return self.P * math.sqrt(self.parent.N) / (1 + self.N)

    def uct_select_children(self):
        child = max(self.children, key = lambda c: c.get_uct_value())
        return child

    def expand(self, actions, Ps):
        for action, P in zip(actions, Ps):
            child = Node(player_id = get_next_player_id(self.player_id), action = action, P = P, parent = self)
            self.children.append(child)

    def update(self, V):
        self.N += 1
        self.W += V
        self.Q = self.W / self.N

class MctsTree:
    def __init__(self, model, root_state, player_id, sim_num, is_training, dirichlet_factor = None, dirichlet_alpha = None):
        self.model = model
        self.sim_num = sim_num
        self.is_training = is_training
        self.dirichlet_factor = dirichlet_factor
        self.dirichlet_alpha = dirichlet_alpha
        self.root_node = Node(player_id = get_next_player_id(player_id))
        self.root_state = copy.deepcopy(root_state)

    def get_legal_Ps(self):
        for sim_id in range(self.sim_num):
            node = self.root_node
            state = copy.deepcopy(self.root_state)

            while not node.is_leaf():
                node = node.uct_select_children()
                state.do_action(node.player_id, node.action)

            result = state.get_result()
            if result>=0:
                V = 1 if result>0 else 0
            else:
                player_id = get_next_player_id(node.player_id)
                state_m = state.to_state_m()
                _, Ps_m, _, V = self.model.evaluate(state_m)
                V = -V
                actions = state.get_legal_actions(player_id)
                action_indexes = [state.action_to_action_index(action) for action in actions]
                legal_Ps_m = Ps_m[action_indexes]
                if self.is_training and not node.parent:
                    legal_Ps_m = legal_Ps_m * (1 - self.dirichlet_factor) + np.random.dirichlet(np.ones_like(legal_Ps_m) * self.dirichlet_alpha) * self.dirichlet_factor
                node.expand(actions, legal_Ps_m)

            while node:
                node.update(V)
                V = -V
                node = node.parent

        #visualize_tree(self.root_node, self.root_state, depth = 3)

        t = 1 if self.is_training else 3
        Ns_m = np.array([c.N for c in self.root_node.children], dtype = np.int64)
        Ns_m **= t
        legal_Ps_m = Ns_m / np.sum(Ns_m)

        return legal_Ps_m

    def get_action(self, state, player_id):
        assert(self.root_state.compact_str()==state.compact_str())
        assert(self.root_node.player_id!=player_id)

        legal_Ps_m = self.get_legal_Ps()

        Ps_m = np.zeros(state.get_action_dim())
        action_indexes = [self.root_state.action_to_action_index(c.action) for c in self.root_node.children]
        Ps_m[action_indexes] = legal_Ps_m

        child = np.random.choice(self.root_node.children, p = legal_Ps_m)
        child.parent = None

        self.root_node = child
        self.root_state.do_action(self.root_node.player_id, self.root_node.action)

        return self.root_node.action, Ps_m

def visualize_tree(root_node, root_state, depth = -1):
    graph = graphviz.Digraph(format = 'svg')
    global_node_id = [0]
    add_graph_node(graph, root_node, root_state, -1, global_node_id, depth)
    graph.render('mcts', cleanup = True)

def add_graph_node(graph, node, state, parent_node_id, global_node_id, depth):
    node_id = global_node_id[0]
    global_node_id[0] += 1
    label = '{0}\n\n{1}'.format(state, node)
    if node.parent:
        exploitation_factor = node.get_uct_value_exploitation_factor()
        exploration_factor = node.get_uct_value_exploration_factor()
        uct_value = exploitation_factor + exploration_factor
        label += '\n\nuct={0:.4f}\nexploitation={1:.4f}\nexploration={2:.4f}'.format(uct_value, exploitation_factor, exploration_factor)
    result = state.get_result()
    if result == 1:
        color = '#ff0000'
    elif result == 2:
        color = '#0000ff'
    elif result == 0:
        color = '#00ff00'
    else:
        color = '#000000'
    if result >= 0:
        style = 'solid'
    else:
        style = 'dashed'
    graph.node(str(node_id), label = label, color = color, fontcolor = color, style = style)
    if node.parent:
        graph.edge(str(parent_node_id), str(node_id))
    if depth>1 or depth==-1:
        for child_node in node.children:
            child_state = copy.deepcopy(state)
            child_state.do_action(child_node.player_id, child_node.action)
            add_graph_node(graph, child_node, child_state, node_id, global_node_id, depth-1 if depth>0 else -1)

