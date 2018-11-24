def main():
    from board_game.states.othello_state import OthelloState
    from board_game.players.othello_player import create_player
    from . import game_regression

    board_shape = (8, 8)
    state = OthelloState(board_shape = board_shape)

    game_regression.main(state, create_player)

