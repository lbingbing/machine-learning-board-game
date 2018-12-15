import itertools
import numpy as np
import os

from .policyvaluenetmcts import MctsTree
from board_game.players.utils import replay_memory
from board_game.players.utils.dynamic_lr import DynamicLR
from board_game.players.utils.utils import get_entropy
from board_game.players.utils.utils import get_cmd_options
from board_game.players.utils.training_monitor import TrainingMonitorContext

def sample(model, rmemory, state, sim_num, dirichlet_factor, dirichlet_alpha, training_monitor):
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
        is_end = (result >= 0)

        if training_monitor != None:
            training_monitor.send_action((player_id, action, is_end))

        if is_end:
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

def main(game_type, get_config):
    title = 'train {0} policyvaluenet model'.format(game_type)

    args = get_cmd_options(title)

    print(title)
    state, model, config = get_config()

    config['replay_memory_file_path'] = os.path.join(os.path.dirname(__file__), '{0}_policyvaluenet_replay_memory.pickle'.format(game_type))

    for k, v in config.items():
        print('{0}: {1}'.format(k, v))

    model_path = config['model_path']
    replay_memory_file_path = config['replay_memory_file_path']
    replay_memory_size = config['replay_memory_size']
    sim_num = config['sim_num']
    dirichlet_factor = config['dirichlet_factor']
    dirichlet_alpha = config['dirichlet_alpha']
    epoch_num = config['epoch_num']
    batch_size = config['batch_size']
    learning_rate = config['learning_rate']
    episode_num = config['episode_num']

    save_flag_file_path = os.path.join(os.path.dirname(__file__), '{0}_policyvaluenet_train.save'.format(game_type))
    saved_flag_file_path = os.path.join(os.path.dirname(__file__), '{0}_policyvaluenet_train.saved'.format(game_type))
    stop_flag_file_path = os.path.join(os.path.dirname(__file__), '{0}_policyvaluenet_train.stop'.format(game_type))
    stopped_flag_file_path = os.path.join(os.path.dirname(__file__), '{0}_policyvaluenet_train.stopped'.format(game_type))

    if os.path.isdir(model_path):
        model.load()
        print('model loaded')
    else:
        model.init_parameters()
        print('model initialized')
    if os.path.isfile(replay_memory_file_path):
        rmemory = replay_memory.load_from_file(replay_memory_file_path)
        print('replay memory loaded')
    else:
        rmemory = replay_memory.ReplayMemory(max_size = replay_memory_size)
        print('replay memory initialized')

    dlr = DynamicLR(lr = learning_rate, min_lr = learning_rate / 100, max_lr = learning_rate, avg_window_size = 80, cmp_window_size = 40)

    with TrainingMonitorContext(args.training_monitor_on) as training_monitor:
        scores = [0] * 3
        for episode_id in range(1, episode_num+1):
            result = sample(model, rmemory, state, sim_num, dirichlet_factor, dirichlet_alpha, training_monitor)
            loss, value_loss, policy_loss, l2_loss = train(model, rmemory, state, epoch_num, batch_size, learning_rate)
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

            if os.path.isfile(save_flag_file_path):
                model.save()
                print('model saved')
                replay_memory.save_to_file(rmemory, replay_memory_file_path)
                print('replay memory saved')
                os.rename(save_flag_file_path, saved_flag_file_path)
            if os.path.isfile(stop_flag_file_path):
                print('stopped')
                os.rename(stop_flag_file_path, stopped_flag_file_path)
                break

