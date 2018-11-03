import random
import itertools
import tensorflow as tf
import numpy as np

import dqn
import replaymemory

#np.set_printoptions(threshold = np.nan)

def sample(model, rmemory, state):
    is_first_action = True
    for player_id in itertools.cycle((1, 2)):
        state_m = state.to_state_m()
        if random.random() < 0.8:
            action = dqn.get_opt_action(model, state)
        else:
            legal_actions = state.get_legal_actions(player_id)
            action = random.choice(legal_actions)
        state.do_action(player_id, action)
        result = state.get_result()
        action_index = state.action_to_action_index(action)
        n_state_m = state.to_state_m()
        n_state_legal_action_mask_m = state.get_legal_action_mask_m()
        r = 1 if result == player_id else 0
        is_end = result>=0

        if not is_first_action:
            if is_end:
                last_r = -1
            rmemory.save((last_state_m, last_action_index, last_r, last_n_state_m, last_n_state_legal_action_mask_m, is_end))
        else:
            is_first_action = False
        if not is_end:
            last_state_m = state_m
            last_action_index = action_index
            last_r = r
            last_n_state_m = n_state_m
            last_n_state_legal_action_mask_m = n_state_legal_action_mask_m
        else:
            rmemory.save((state_m, action_index, r, n_state_m, n_state_legal_action_mask_m, is_end))
            break

def train(model, rmemory, action_dim, discount, batch_size, learning_rate, epoch_num):
    losses = []
    for epoch_id in range(epoch_num):
        transitions = [rmemory.sample() for i in range(batch_size)]
        state_m_l, action_index_l, r_l, n_state_m_l, n_state_legal_action_mask_m_l, is_end_l = zip(*transitions)
        state_m_batch = np.concatenate(state_m_l, axis = 0)
        n_state_m_batch = np.concatenate(n_state_m_l, axis = 0)
        n_state_legal_action_mask_m_batch = np.concatenate(n_state_legal_action_mask_m_l, axis = 0)
        Q_mask_batch = np.zeros((batch_size, action_dim))
        for sample_id, action_index in enumerate(action_index_l):
            Q_mask_batch[sample_id, action_index] = 1
        _, max_n_Q_m_batch = dqn.get_max_Q_m(model, n_state_m_batch, n_state_legal_action_mask_m_batch)
        is_end_m_batch = np.array(is_end_l).reshape(-1, 1)
        target_Q_m_batch = np.array(r_l).reshape(-1, 1).astype(dtype = np.float32)
        target_Q_m_batch += np.where(is_end_m_batch, 0, max_n_Q_m_batch) * discount
        target_Q_m_batch = target_Q_m_batch * Q_mask_batch
        loss = model.train(state_m_batch, target_Q_m_batch, Q_mask_batch, learning_rate)
        losses.append(loss)
    return sum(losses) / len(losses)

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
        model_name = 'gomoku_dqn_model_{0}_{1}_{2}'.format(board_shape[0], board_shape[1], target)
        replaymemory_file_path = 'gomoku_dqn_replaymemory.pickle'
    elif game_name == 'Chess':
        import chessstate

        print('Game: Chess')
        state = chessstate.ChessState()
        model_name = 'chess_dqn_model'
        replaymemory_file_path = 'chess_dqn_replaymemory.pickle'

    replaymemory_size = 64 * 1024
    discount = 0.95
    batch_size = 16
    epoch_num = 4
    learning_rate = 0.001
    episode_num = 2000000

    print('replaymemory_size:', replaymemory_size)
    print('discount:', discount)
    print('batch_size:', batch_size)
    print('epoch_num:', epoch_num)
    print('learning_rate:', learning_rate)
    print('episode_num:', episode_num)

    model = dqn.DqnModel(board_shape = state.board_shape, action_dim = state.get_action_dim(), model_name = model_name)
    model.init_parameters()
    #model.load()
    rmemory = replaymemory.ReplayMemory(max_size = replaymemory_size)
    if os.path.isfile(replaymemory_file_path):
        rmemory = replaymemory.loadfromfile(replaymemory_file_path)
    scores = [0] * 3
    for episode_id in range(1, episode_num+1):
        state.reset()
        sample(model, rmemory, state)
        loss = train(model, rmemory, state.get_action_dim(), discount, batch_size, learning_rate, epoch_num)
        result = state.get_result()
        scores[result] += 1
        if episode_id % 1 == 0:
            state.reset()
            max_Q_logit1, max_Q1 = map(np.asscalar, dqn.get_max_Q_m(model, state.to_state_m(), state.get_legal_action_mask_m()))
            state_m = state.to_state_m()
            action = dqn.get_opt_action(model, state)
            state.do_action(1, action)
            max_Q_logit2, max_Q2 = map(np.asscalar, dqn.get_max_Q_m(model, state.to_state_m(), state.get_legal_action_mask_m()))
            print('episode: {0} L: {1:.8f} m_Q_l1: {2:.2f} m_Q1: {3:.6f} m_Q_l2: {4:.2f} m_Q2: {5:.6f} p1/p2/draw: {6}/{7}/{8}'.format(episode_id, loss, max_Q_logit1, max_Q1, max_Q_logit2, max_Q2, scores[1], scores[2], scores[0]))
        #model.save()
        #replaymemory.savetofile(rmemory, replaymemory_file_path)
        if os.path.isfile('dqn_train_stop'):
            print('stopped')
            break

if __name__ == '__main__':
    main()

