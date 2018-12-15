import argparse
import itertools
import os

from .utils import get_cmd_options
from board_game.players.player import is_human
from board_game.players.player import is_monitor
from board_game.games.utils import save_transcript

def main(game_type, state, create_player):
    args = get_cmd_options(game_type+' cmd game')

    player1 = create_player(state, args.player_type1, 1)
    player2 = create_player(state, args.player_type2, 2)
    is_save_transcript = args.save_transcript
    is_monitor_mode = (is_monitor(player1) and is_monitor(player2))

    while True:
        state.reset()
        print(state)
        actions = []
        for step, p in enumerate(itertools.cycle((player1, player2))):
            print('[{0}] {1}({2}) action:'.format(step, p.type, p.player_id), end = '', flush = True)
            action = p.get_action(state)
            state.do_action(p.player_id, action)
            actions.append(action)
            if not is_human(p):
                print(action)
            print(state)
            if not is_monitor_mode:
                input('pause')
            result = state.get_result()
            if result >= 0:
                if result > 0:
                    print('player {0} wins'.format(result))
                else:
                    print('draw')
                if is_save_transcript:
                    save_transcript(os.path.join(os.path.dirname(__file__), game_type+'.trans'), actions)
                break

