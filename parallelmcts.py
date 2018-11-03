import random
import math
import copy
import concurrent.futures
import graphviz

from utils import get_next_player_id

class Node:
    def __init__(self, state, player_id, action, parent):
        self.player_id = player_id # player_id that takes the action
        self.action = action # the action that player takes
        self.N = 0
        self.W = 0
        self.Q = 0

        self.unexpanded_actions = state.get_legal_actions(get_next_player_id(player_id))
        self.children = []
        self.parent = parent

    def __str__(self):
        return 'player={0}\naction={1}\nN={2}\nW={3}\nQ={4}'.format(self.player_id, self.action, self.N, self.W, self.Q)

    def is_fully_expanded(self):
        return len(self.unexpanded_actions) == 0

    def add_child(self, child):
        self.unexpanded_actions.remove(child.action)
        self.children.append(child)

    def get_uct_value(self):
        return self.get_uct_value_exploitation_factor() + self.get_uct_value_exploration_factor()

    def get_uct_value_exploitation_factor(self):
        return self.Q

    def get_uct_value_exploration_factor(self):
        return math.sqrt(2 * math.log(self.parent.N) / self.N)

    def uct_select_children(self):
        child = max(self.children, key = lambda c: c.get_uct_value())
        return child

    def update(self, V):
        self.N += 1
        self.W += V
        self.Q = self.W / self.N

def search(root_node, root_state, sim_num):
    state = copy.deepcopy(root_state)
    for sim_id in range(sim_num):
        node = root_node
        state.copy(root_state)

        while not state.is_end() and node.is_fully_expanded():
            node = node.uct_select_children()
            state.do_action(node.player_id, node.action)

        if not state.is_end():
            action = random.choice(node.unexpanded_actions)
            next_player_id = get_next_player_id(node.player_id)
            state.do_action(next_player_id, action)
            child = Node(state = state, player_id = next_player_id, action = action, parent = node)
            node.add_child(child)
            node = child

        player_id = node.player_id
        while not state.is_end():
            player_id = get_next_player_id(player_id)
            action = random.choice(state.get_legal_actions(player_id))
            state.do_action(player_id, action)

        result = state.get_result()
        if result > 0:
            V = 1 if result == node.player_id else -1
        else:
            V = 0

        while node:
            node.update(V)
            V = -V
            node = node.parent

    action_to_N = {c.action : c.N for c in root_node.children}
    return action_to_N

class MctsTree:
    def __init__(self, executor, root_state, player_id, sim_num):
        self.sim_num = sim_num
        self.executor = executor
        self.root_node = Node(state = root_state, player_id = get_next_player_id(player_id), action = None, parent = None)
        self.root_state = copy.deepcopy(root_state)

    def get_action(self, state, player_id):
        assert(self.root_state.compact_str()==state.compact_str())
        assert(self.root_node.player_id!=player_id)

        root_node = self.root_node
        root_state = copy.deepcopy(self.root_state)
        futures = [self.executor.submit(search, root_node, root_state, self.sim_num) for i in range(4)]
        action_to_N_l = [future.result() for future in concurrent.futures.as_completed(futures)]
        action_to_N_total = {}
        for action_to_N in action_to_N_l:
            for action, N in action_to_N.items():
                if action not in action_to_N_total:
                    action_to_N_total[action] = 0
                action_to_N_total[action] += N
        action = max(action_to_N_total, key = lambda a: action_to_N_total[a])
        return action

        #visualize_tree(self.root_node, self.root_state, depth = 3)

        #child = max(self.root_node.children, key = lambda c: c.N)
        #child.parent = None

        #self.root_node = child
        #self.root_state.do_action(self.root_node.player_id, self.root_node.action)

        #return self.root_node.action

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
        uct_value = node.get_uct_value()
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
    if result >= 0 or node.is_fully_expanded():
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

