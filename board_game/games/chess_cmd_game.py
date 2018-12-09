def main():
    from board_game.states.chess_state import ChessState
    from board_game.players.chess_player import create_player
    from . import cmd_game

    state = ChessState()

    cmd_game.main('chess', state, create_player)

