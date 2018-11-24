import itertools

from board_game.players import player

def main(state, create_player):
    import sys

    player_types = player.parse_cmd_player_types()
    player1, player2 = [create_player(state, player_type, player_id) for player_id, player_type in enumerate(player_types, 1)]

    game_num = 100
    results = [0] * 3
    print_progress = lambda: print('\rpl/p2/draw/total: {0}/{1}/{2}/{3}'.format(results[1], results[2], results[0], game_num), end = '', file = sys.stderr, flush = True)
    print_progress()
    for game_id in range(game_num):
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

