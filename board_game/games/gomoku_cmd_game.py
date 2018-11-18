def main():
    from board_game.states.gomoku_state import GomokuState
    from board_game.players.gomoku_player import create_player
    from . import cmd_game

    board_shape = (9, 9)
    target = 5
    state = GomokuState(board_shape = board_shape, target = target)

    cmd_game.main(state, create_player)

