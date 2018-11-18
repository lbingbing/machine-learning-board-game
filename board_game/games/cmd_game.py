import itertools

from board_game.players import player

def main(state, create_player):
    player_types = player.parse_cmd_player_types()
    player1, player2 = [create_player(state, player_type, player_id) for player_id, player_type in enumerate(player_types, 1)]

    state.reset()
    print(state)
    for step, p in enumerate(itertools.cycle((player1, player2))):
        print('[{0}] {1}({2}) action:'.format(step, p.type, p.player_id), end = '', flush = True)
        action = p.get_action(state)
        state.do_action(p.player_id, action)
        if not player.is_human(p):
            print(action)
        print(state)
        input('pause')
        result = state.get_result()
        if result >= 0:
            if result > 0:
                print('player {0} wins'.format(result))
            else:
                print('draw')
            break

