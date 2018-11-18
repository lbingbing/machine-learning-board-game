def main():
    from .tictactoe_state import TicTacToeState

    state = TicTacToeState(board_shape = (3, 3))
    state.board = [[1,2,1],
                   [1,1,2],
                   [2,2,1]]
    state.last_player_id = 1
    state.piece_num = 9
    state.last_action = (0, 0)
    assert(state.get_result()==1)
    state.last_action = (1, 1)
    assert(state.get_result()==1)
    state.last_action = (2, 2)
    assert(state.get_result()==1)
    state.board = [[1,2,1],
                   [1,2,1],
                   [2,2,0]]
    state.last_player_id = 2
    state.piece_num = 8
    state.last_action = (0, 1)
    assert(state.get_result()==2)
    state.last_action = (1, 1)
    assert(state.get_result()==2)
    state.last_action = (1, 1)
    assert(state.get_result()==2)

    print('pass')

