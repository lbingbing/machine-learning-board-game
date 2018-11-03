import itertools
import numpy as np

import policyvaluenet
import replaymemory
import policyvaluenetmcts
import dynamiclr

def sample(model, rmemory, state, sim_num, dirichlet_factor, dirichlet_alpha):
    state_m_l = []
    Ps_m_l = []
    state.reset()
    mcts_tree = policyvaluenetmcts.MctsTree(model = model, root_state = state, player_id = 1, sim_num = sim_num, self_play = True, dirichlet_factor = dirichlet_factor, dirichlet_alpha = dirichlet_alpha)
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

def main():
    import os

    game_name = 'Gomoku'
    #game_name = 'Chess'

    if game_name == 'Gomoku':
        import blackwhitestate

        print('Game: Gomoku')
        board_shape = (9, 9)
        target = 5
        print('board_shape:', board_shape)
        print('target:', target)

        state = blackwhitestate.GomokuState(board_shape = board_shape, target = target)
        model_name = 'gomoku_policyvaluenet_model_{0}_{1}_{2}'.format(board_shape[0], board_shape[1], target)
        replaymemory_file_path = 'gomoku_policyvaluenet_replaymemory.pickle'
    elif game_name == 'Chess':
        import chessstate

        print('Game: Chess')
        state = chessstate.ChessState()
        model_name = 'chess_policyvaluenet_model'
        replaymemory_file_path = 'chess_policyvaluenet_replaymemory.pickle'

    replaymemory_size = 64 * 1024
    #sim_num = 1000
    sim_num = 5
    dirichlet_factor = 0.25
    dirichlet_alpha = 0.03
    #epoch_num = 16
    epoch_num = 1
    #batch_size = 128
    batch_size = 1
    learning_rate = 0.003
    episode_num = 2000000

    print('replaymemory_size:', replaymemory_size)
    print('sim_num:', sim_num)
    print('dirichlet_factor:', dirichlet_factor)
    print('dirichlet_alpha:', dirichlet_alpha)
    print('epoch_num:', epoch_num)
    print('batch_size:', batch_size)
    print('learning_rate:', learning_rate)
    print('episode_num:', episode_num)

    model = policyvaluenet.PolicyValueNetModel(board_shape = state.board_shape, action_dim = state.get_action_dim(), model_name = model_name)
    model.init_parameters()
    #model.load()
    rmemory = replaymemory.ReplayMemory(max_size = replaymemory_size)
    if os.path.isfile(replaymemory_file_path):
        rmemory = replaymemory.loadfromfile(replaymemory_file_path)
    scores = [0] * 3
    dlr = dynamiclr.DynamicLR(lr = learning_rate, min_lr = learning_rate / 100, max_lr = learning_rate, avg_window_size = 80, cmp_window_size = 40)
    for episode_id in range(1, episode_num+1):
        result = sample(model, rmemory, state, sim_num, dirichlet_factor, dirichlet_alpha)
        loss, value_loss, policy_loss, l2_loss = train(model, rmemory, state, epoch_num, batch_size, learning_rate)
        scores[result] += 1
        state.reset()
        state_m = state.to_state_m()
        P_logits_m, Ps_m, V_logit, V = model.evaluate(state_m)
        min_P_logit = np.min(P_logits_m)
        max_P_logit = np.max(P_logits_m)
        entropy = policyvaluenet.get_entropy(Ps_m)
        print('episode: {0} L: {1:.4f} ({2:.4f}/{3:.4f}/{4:.4f}) P_l: ({5:.2f}, {6:.2f}) P_e: {7:.6f} V_l: {8:.2f} V: {9:.6f} p1/p2/draw: {10}/{11}/{12}'.format(episode_id, loss, value_loss, policy_loss, l2_loss, min_P_logit, max_P_logit, entropy, V_logit, V, scores[1], scores[2], scores[0]))
        if dlr.update(loss):
            print('adjust learning_rate: {0} -> {1}'.format(learning_rate, dlr.lr))
            learning_rate = dlr.lr

        #model.save()
        #replaymemory.savetofile(rmemory, replaymemory_file_path)
        if os.path.isfile('policyvaluenet_train_stop'):
            print('stopped')
            break

if __name__ == '__main__':
    main()

