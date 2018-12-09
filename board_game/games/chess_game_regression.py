def main():
    from board_game.states.chess_state import ChessState
    from board_game.players.chess_player import create_player
    from . import game_regression

    state = ChessState()

    game_regression.main('chess', state, create_player)

