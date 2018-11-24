from .blackwhite_state import BlackWhiteState

class TicTacToeState(BlackWhiteState):
    def __init__(self, board_shape):
        super().__init__(board_shape)
        assert(board_shape[0]==board_shape[1])

    def reset(self):
        super().reset()
        self.legal_actions = set((i, j) for i in range(self.board_shape[0]) for j in range(self.board_shape[1]))

    def copy(self, rhs):
        super().copy(rhs)
        self.legal_actions = set(rhs.legal_actions)

    def get_legal_actions(self, player_id):
        super().get_legal_actions(player_id)
        return tuple(self.legal_actions)

    def get_result(self):
        if self.last_action == None:
            return -1
        # row
        for j in range(self.board_shape[1]):
            if self.board[self.last_action[0]][j] != self.last_player_id:
                break
        else:
            return self.last_player_id
        # column
        for i in range(self.board_shape[0]):
            if self.board[i][self.last_action[1]] != self.last_player_id:
                break
        else:
            return self.last_player_id
        # diagonal 1
        for i in range(self.board_shape[0]):
            if self.board[i][i] != self.last_player_id:
                break
        else:
            return self.last_player_id
        # diagonal 2
        for i in range(self.board_shape[0]):
            if self.board[i][self.board_shape[0]-i-1] != self.last_player_id:
                break
        else:
            return self.last_player_id
        # draw or not end yet
        return 0 if self.piece_num == self.board_shape[0] * self.board_shape[1] else -1

    def do_action(self, player_id, action):
        super().do_action(player_id, action)
        self.legal_actions.remove(action)

