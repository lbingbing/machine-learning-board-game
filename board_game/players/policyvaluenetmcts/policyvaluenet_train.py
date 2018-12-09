import itertools
import numpy as np
import os

from .policyvaluenetmcts import MctsTree
from board_game.players.utils import replaymemory
from board_game.players.utils.dynamiclr import DynamicLR
from board_game.players.utils.utils import get_entropy

def sample(model, rmemory, state, sim_num, dirichlet_factor, dirichlet_alpha):
    state_m_l = []
    Ps_m_l = []
    state.reset()
    mcts_tree = MctsTree(model = model, root_state = state, player_id = 1, sim_num = sim_num, is_training = True, dirichlet_factor = dirichlet_factor, dirichlet_alpha = dirichlet_alpha)
    for player_id in itertools.cycle((1, 2)):
        state_m = state.to_state_m()
        state_m_l.append(state_m)
        action, Ps_m = mcts_tree.get_action(state, player_id)
        Ps_m_l.append(Ps_m.reshape(1, -1))
        state.do_action(player_id, action)
        result = state.get_result()
        if result >= 0:
            break
    if result == 1:
        V = 1
    elif result == 2:
        V = -1
    else:
        V = 0
    V_m = np.array(V).reshape(1, 1)
    V_m_l = [V_m * ((-1) ** i) for i in range(len(state_m_l))]

    for state_m, Ps_m, V_m in zip(state_m_l, Ps_m_l, V_m_l):
        samples = rmemory.save((state_m, Ps_m, V_m))

    return result

def train(model, rmemory, state, epoch_num, batch_size, learning_rate):
    losses = []
    for epoch_id in range(epoch_num):
        samples = [rmemory.sample() for i in range(batch_size)]
        state_m_batch_l = []
        Ps_m_batch_l = []
        V_m_batch_l = []
        for state_m, Ps_m, V_m in samples:
            state_m_batch = state.get_equivalent_state_m_batch(state_m)
            state_m_batch_l.append(state_m_batch)
            Ps_m_batch = state.get_equivalent_Ps_m_batch(Ps_m, state.board_shape)
            Ps_m_batch_l.append(Ps_m_batch)
            V_m_batch = state.get_equivalent_V_m_batch(V_m)
            V_m_batch_l.append(V_m_batch)
        state_m_batch = np.concatenate(state_m_batch_l)
        Ps_m_batch = np.concatenate(Ps_m_batch_l)
        V_m_batch = np.concatenate(V_m_batch_l)
        loss, value_loss, policy_loss, l2_loss = model.train(state_m_batch, Ps_m_batch, V_m_batch, learning_rate)
        losses.append((loss, value_loss, policy_loss, l2_loss))
    return (sum(e) / len(losses) for e in zip(*losses))

def main(state, model, config):
    for k, v in config.items():
        print('{0}: {1}'.format(k, v))

    learning_rate = config['learning_rate']

    if os.path.isdir(config['model_path']):
        model.load()
        print('model loaded')
    else:
        model.init_parameters()
        print('model initialized')
    if os.path.isfile(config['replaymemory_file_path']):
        rmemory = replaymemory.loadfromfile(config['replaymemory_file_path'])
        print('replay memory loaded')
    else:
        rmemory = replaymemory.ReplayMemory(max_size = config['replaymemory_size'])
        print('replay memory initialized')
    scores = [0] * 3
    dlr = DynamicLR(lr = learning_rate, min_lr = learning_rate / 100, max_lr = learning_rate, avg_window_size = 80, cmp_window_size = 40)
    for episode_id in range(1, config['episode_num']+1):
        result = sample(model, rmemory, state, config['sim_num'], config['dirichlet_factor'], config['dirichlet_alpha'])
        loss, value_loss, policy_loss, l2_loss = train(model, rmemory, state, config['epoch_num'], config['batch_size'], learning_rate)
        scores[result] += 1
        state.reset()
        state_m = state.to_state_m()
        P_logits_m, Ps_m, V_logit, V = model.evaluate(state_m)
        min_P_logit = np.min(P_logits_m)
        max_P_logit = np.max(P_logits_m)
        entropy = get_entropy(Ps_m)
        print('episode: {0} L: {1:.4f} ({2:.4f}/{3:.4f}/{4:.4f}) P_l: ({5:.2f}, {6:.2f}) P_e: {7:.6f} V_l: {8:.2f} V: {9:.6f} p1/p2/draw: {10}/{11}/{12}'.format(episode_id, loss, value_loss, policy_loss, l2_loss, min_P_logit, max_P_logit, entropy, V_logit, V, scores[1], scores[2], scores[0]))
        if dlr.update(loss):
            print('adjust learning_rate: {0} -> {1}'.format(learning_rate, dlr.lr))
            learning_rate = dlr.lr

        if os.path.isfile(config['save_flag_file_path']):
            model.save()
            print('model saved')
            replaymemory.savetofile(rmemory, config['replaymemory_file_path'])
            print('replay memory saved')
            os.rename(config['save_flag_file_path'], config['saved_flag_file_path'])
        if os.path.isfile(config['stop_flag_file_path']):
            print('stopped')
            break

