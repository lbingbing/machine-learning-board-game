def main():
    from .gomoku_state import GomokuState

    state = GomokuState(board_shape = (7, 7))
    state.board = [[1,1,1,1,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0]]
    state.last_player_id = 1
    state.piece_num = 4
    state.last_action = (0, 0)
    assert(state.get_result()==-1)
    state.last_action = (0, 2)
    assert(state.get_result()==-1)
    state.last_action = (0, 3)
    assert(state.get_result()==-1)
    state.board = [[1,1,1,1,1,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0]]
    state.last_player_id = 1
    state.piece_num = 5
    state.last_action = (0, 0)
    assert(state.get_result()==1)
    state.last_action = (0, 2)
    assert(state.get_result()==1)
    state.last_action = (0, 4)
    assert(state.get_result()==1)
    state.board = [[0,2,2,2,2,2,2],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0]]
    state.last_player_id = 2
    state.piece_num = 6
    state.last_action = (0, 1)
    assert(state.get_result()==2)
    state.last_action = (0, 4)
    assert(state.get_result()==2)
    state.last_action = (0, 6)
    assert(state.get_result()==2)
    state.board = [[0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [1,1,1,1,1,0,0]]
    state.last_player_id = 1
    state.piece_num = 5
    state.last_action = (6, 0)
    assert(state.get_result()==1)
    state.last_action = (6, 2)
    assert(state.get_result()==1)
    state.last_action = (6, 4)
    assert(state.get_result()==1)
    state.board = [[0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,2,2,2,2,2,2]]
    state.last_player_id = 2
    state.piece_num = 6
    state.last_action = (6, 1)
    assert(state.get_result()==2)
    state.last_action = (6, 4)
    assert(state.get_result()==2)
    state.last_action = (6, 6)
    assert(state.get_result()==2)
    state.board = [[1,0,0,0,0,0,0],
                   [1,0,0,0,0,0,0],
                   [1,0,0,0,0,0,0],
                   [1,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0]]
    state.last_player_id = 1
    state.piece_num = 4
    state.last_action = (0, 0)
    assert(state.get_result()==-1)
    state.last_action = (2, 0)
    assert(state.get_result()==-1)
    state.last_action = (3, 0)
    assert(state.get_result()==-1)
    state.board = [[1,0,0,0,0,0,0],
                   [1,0,0,0,0,0,0],
                   [1,0,0,0,0,0,0],
                   [1,0,0,0,0,0,0],
                   [1,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0]]
    state.last_player_id = 1
    state.piece_num = 5
    state.last_action = (0, 0)
    assert(state.get_result()==1)
    state.last_action = (2, 0)
    assert(state.get_result()==1)
    state.last_action = (4, 0)
    assert(state.get_result()==1)
    state.board = [[0,0,0,0,0,0,0],
                   [2,0,0,0,0,0,0],
                   [2,0,0,0,0,0,0],
                   [2,0,0,0,0,0,0],
                   [2,0,0,0,0,0,0],
                   [2,0,0,0,0,0,0],
                   [2,0,0,0,0,0,0]]
    state.last_player_id = 2
    state.piece_num = 6
    state.last_action = (1, 0)
    assert(state.get_result()==2)
    state.last_action = (4, 0)
    assert(state.get_result()==2)
    state.last_action = (6, 0)
    assert(state.get_result()==2)
    state.board = [[0,0,0,0,0,0,1],
                   [0,0,0,0,0,0,1],
                   [0,0,0,0,0,0,1],
                   [0,0,0,0,0,0,1],
                   [0,0,0,0,0,0,1],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0]]
    state.last_player_id = 1
    state.piece_num = 5
    state.last_action = (0, 6)
    assert(state.get_result()==1)
    state.last_action = (2, 6)
    assert(state.get_result()==1)
    state.last_action = (4, 6)
    assert(state.get_result()==1)
    state.board = [[0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,2],
                   [0,0,0,0,0,0,2],
                   [0,0,0,0,0,0,2],
                   [0,0,0,0,0,0,2],
                   [0,0,0,0,0,0,2],
                   [0,0,0,0,0,0,2]]
    state.last_player_id = 2
    state.piece_num = 6
    state.last_action = (1, 6)
    assert(state.get_result()==2)
    state.last_action = (4, 6)
    assert(state.get_result()==2)
    state.last_action = (6, 6)
    assert(state.get_result()==2)
    state.board = [[1,0,0,0,0,0,0],
                   [0,1,0,0,0,0,0],
                   [0,0,1,0,0,0,0],
                   [0,0,0,1,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0]]
    state.last_player_id = 1
    state.piece_num = 4
    state.last_action = (0, 0)
    assert(state.get_result()==-1)
    state.last_action = (2, 2)
    assert(state.get_result()==-1)
    state.last_action = (3, 3)
    assert(state.get_result()==-1)
    state.board = [[1,0,0,0,0,0,0],
                   [0,1,0,0,0,0,0],
                   [0,0,1,0,0,0,0],
                   [0,0,0,1,0,0,0],
                   [0,0,0,0,1,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0]]
    state.last_player_id = 1
    state.piece_num = 5
    state.last_action = (0, 0)
    assert(state.get_result()==1)
    state.last_action = (2, 2)
    assert(state.get_result()==1)
    state.last_action = (4, 4)
    assert(state.get_result()==1)
    state.board = [[0,0,0,0,0,0,0],
                   [0,2,0,0,0,0,0],
                   [0,0,2,0,0,0,0],
                   [0,0,0,2,0,0,0],
                   [0,0,0,0,2,0,0],
                   [0,0,0,0,0,2,0],
                   [0,0,0,0,0,0,2]]
    state.last_player_id = 2
    state.piece_num = 6
    state.last_action = (1, 1)
    assert(state.get_result()==2)
    state.last_action = (4, 4)
    assert(state.get_result()==2)
    state.last_action = (6, 6)
    assert(state.get_result()==2)
    state.board = [[0,0,0,0,0,0,1],
                   [0,0,0,0,0,1,0],
                   [0,0,0,0,1,0,0],
                   [0,0,0,1,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0]]
    state.last_player_id = 1
    state.piece_num = 4
    state.last_action = (0, 6)
    assert(state.get_result()==-1)
    state.last_action = (2, 4)
    assert(state.get_result()==-1)
    state.last_action = (3, 3)
    assert(state.get_result()==-1)
    state.board = [[0,0,0,0,0,0,1],
                   [0,0,0,0,0,1,0],
                   [0,0,0,0,1,0,0],
                   [0,0,0,1,0,0,0],
                   [0,0,1,0,0,0,0],
                   [0,0,0,0,0,0,0],
                   [0,0,0,0,0,0,0]]
    state.last_player_id = 1
    state.piece_num = 5
    state.last_action = (0, 6)
    assert(state.get_result()==1)
    state.last_action = (2, 4)
    assert(state.get_result()==1)
    state.last_action = (4, 2)
    assert(state.get_result()==1)
    state.board = [[0,0,0,0,0,0,0],
                   [0,0,0,0,0,2,0],
                   [0,0,0,0,2,0,0],
                   [0,0,0,2,0,0,0],
                   [0,0,2,0,0,0,0],
                   [0,2,0,0,0,0,0],
                   [2,0,0,0,0,0,0]]
    state.last_player_id = 2
    state.piece_num = 6
    state.last_action = (6, 0)
    assert(state.get_result()==2)
    state.last_action = (4, 2)
    assert(state.get_result()==2)
    state.last_action = (1, 5)
    assert(state.get_result()==2)

    state = GomokuState(board_shape = (5, 5), target = 4)
    state.board = [[0,0,0,0,0],
                   [2,1,1,1,1],
                   [0,2,1,0,0],
                   [0,2,0,2,0],
                   [0,0,0,0,0]]
    state.last_player_id = 1
    state.piece_num = 9
    state.last_action = (1, 4)
    assert(state.get_result()==1)
    state.board = [[2, 2, 1, 2, 1],
                   [1, 2, 1, 1, 2],
                   [2, 1, 1, 1, 1],
                   [2, 2, 1, 2, 1],
                   [1, 2, 2, 1, 2]]
    state.last_player_id = 1
    state.piece_num = 25
    state.last_action = (0, 2)
    assert(state.get_result()==1)

    print('pass')

