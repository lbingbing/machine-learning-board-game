def get_cmd_options(title):
    import argparse
    from board_game.players import player

    parser = argparse.ArgumentParser(description=title)
    parser.add_argument('player_type1', choices=player.PLAYER_TYPES, help='player1 type')
    parser.add_argument('player_type2', choices=player.PLAYER_TYPES, help='player2 type')
    parser.add_argument('--save_transcript', action='store_true', help='save transcript')
    args = parser.parse_args()
    return args

