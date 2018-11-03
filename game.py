import itertools

import blackwhitestate
import player

def regress():
    import sys

    #state_factory = lambda: blackwhitestate.TicTacToeState(board_size = 3)
    board_size = 7
    target = 4
    state_factory = lambda: blackwhitestate.GomokuState(board_size = board_size, target = target)
    state = state_factory()
    #player1 = player.RandomPlayer(player_id = 1)
    player1 = player.MctsPlayer(player_id = 1, sim_num = 1000)
    #player2 = player.RandomPlayer(player_id = 2)
    player2 = player.MctsPlayer(player_id = 2, sim_num = 1000)
    results = [0] * 3
    print_progress = lambda: print('\rpl/p2/draw: {0}/{1}/{2}'.format(results[1], results[2], results[0]), end = '', file = sys.stderr, flush = True)
    print_progress()
    for game_id in range(10):
        state.reset()
        for step, p in enumerate(itertools.cycle((player1, player2))):
            action = p.get_action(state)
            state.do_action(p.player_id, action)
            result = state.get_result()
            if result >= 0:
                results[result] += 1
                break
        print_progress()
    print(file = sys.stderr)

def check_end(state):
    result = state.get_result()
    if result >= 0:
        if result > 0:
            print('player {0} wins'.format(result))
        else:
            print('draw')
        return True
    else:
        return False

def main():
    #state_factory = lambda: blackwhitestate.TicTacToeState(board_size = 3)
    board_size = 9
    target = 5
    state_factory = lambda: blackwhitestate.GomokuState(board_size = board_size, target = target)
    state = state_factory()
    #player1 = player.RandomPlayer(player_id = 1)
    #player1 = player.MctsPlayer(player_id = 1, sim_num = 10000)
    #player1 = player.ParallelMctsPlayer(player_id = 1, sim_num = 5000)
    #player1 = player.DqnPlayer(player_id = 1, board_size = board_size, target = target)
    #player1 = player.PolicyNetPlayer(player_id = 1, board_size = board_size, target = target)
    player1 = player.PolicyValueNetMctsPlayer(player_id = 1, board_size = board_size, target = target, sim_num = 1000)
    #player1 = player.HumanPlayer(player_id = 1)
    #player2 = player.RandomPlayer(player_id = 2)
    #player2 = player.MctsPlayer(player_id = 2, sim_num = 10000)
    #player2 = player.ParallelMctsPlayer(player_id = 2, sim_num = 5000)
    #player2 = player.DqnPlayer(player_id = 2, board_size = board_size, target = target)
    #player2 = player.PolicyNetPlayer(player_id = 2, board_size = board_size, target = target)
    player2 = player.PolicyValueNetMctsPlayer(player_id = 2, board_size = board_size, target = target, sim_num = 1000)
    #player2 = player.HumanPlayer(player_id = 2)
    for game_id in range(20):
        print('==== game {0} ===='.format(game_id))
        state.reset()
        print(state)
        for step, p in enumerate(itertools.cycle((player1, player2))):
            print('[{0}] {1}({2}) action:'.format(step, p.name, p.player_id), end = '', flush = True)
            action = p.get_action(state)
            state.do_action(p.player_id, action)
            if not p.ishuman:
                print('{0},{1}'.format(action[0], action[1]))
            print(state)
            input('pause')
            if check_end(state):
                break

if __name__ == '__main__':
    #regress()
    main()

