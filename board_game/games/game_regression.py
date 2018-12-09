import argparse
import sys
import itertools
import os

from .utils import get_cmd_options
from board_game.utils.utils import save_transcript

def main(game_type, state, create_player):
    args = get_cmd_options(game_type+' game regression')

    player1 = create_player(state, args.player_type1, 1)
    player2 = create_player(state, args.player_type2, 2)
    is_save_transcript = args.save_transcript

    game_num = 100
    results = [0] * 3
    print_progress = lambda: print('\rpl/p2/draw/total: {0}/{1}/{2}/{3}'.format(results[1], results[2], results[0], game_num), end = '', file = sys.stderr, flush = True)
    print_progress()
    for game_id in range(game_num):
        state.reset()
        actions = []
        for step, p in enumerate(itertools.cycle((player1, player2))):
            action = p.get_action(state)
            state.do_action(p.player_id, action)
            actions.append(action)
            result = state.get_result()
            if result >= 0:
                results[result] += 1
                if is_save_transcript:
                    save_transcript(os.path.join(os.path.dirname(__file__), game_type+str(game_id)+'.trans'), actions)
                break
        print_progress()
    print(file = sys.stderr)

