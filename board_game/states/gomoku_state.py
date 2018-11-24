from .blackwhite_state import BlackWhiteState

class GomokuState(BlackWhiteState):
    def __init__(self, board_shape, target = 5):
        super().__init__(board_shape)
        self.target = target

    def reset(self):
        super().reset()
        self.legal_actions = set((i, j) for i in range(self.board_shape[0]) for j in range(self.board_shape[1]))

    def copy(self, rhs):
        super().copy(rhs)
        self.target = rhs.target
        self.legal_actions = set(rhs.legal_actions)

    def get_legal_actions(self, player_id):
        super().get_legal_actions(player_id)
        return tuple(self.legal_actions)

    def get_result(self):
        if self.last_action == None:
            return -1
        # row
        j1 = self.last_action[1]
        while j1-1 >= 0 and self.board[self.last_action[0]][j1-1] == self.last_player_id:
            j1 -= 1
        j2 = self.last_action[1]
        while j2+1 < self.board_shape[1] and self.board[self.last_action[0]][j2+1] == self.last_player_id:
            j2 += 1
        if j2-j1+1 >= self.target:
            return self.last_player_id
        # column
        i1 = self.last_action[0]
        while i1-1 >= 0 and self.board[i1-1][self.last_action[1]] == self.last_player_id:
            i1 -= 1
        i2 = self.last_action[0]
        while i2+1 < self.board_shape[0] and self.board[i2+1][self.last_action[1]] == self.last_player_id:
            i2 += 1
        if i2-i1+1 >= self.target:
            return self.last_player_id
        # diagonal 1
        i1 = self.last_action[0]
        j1 = self.last_action[1]
        while i1-1 >= 0 and j1-1 >= 0 and self.board[i1-1][j1-1] == self.last_player_id:
            i1 -= 1
            j1 -= 1
        i2 = self.last_action[0]
        j2 = self.last_action[1]
        while i2+1 < self.board_shape[0] and j2+1 < self.board_shape[1] and self.board[i2+1][j2+1] == self.last_player_id:
            i2 += 1
            j2 += 1
        if i2-i1+1 >= self.target:
            return self.last_player_id
        # diagonal 2
        i1 = self.last_action[0]
        j1 = self.last_action[1]
        while i1-1 >= 0 and j1+1 < self.board_shape[1] and self.board[i1-1][j1+1] == self.last_player_id:
            i1 -= 1
            j1 += 1
        i2 = self.last_action[0]
        j2 = self.last_action[1]
        while i2+1 < self.board_shape[0] and j2-1 >= 0 and self.board[i2+1][j2-1] == self.last_player_id:
            i2 += 1
            j2 -= 1
        if i2-i1+1 >= self.target:
            return self.last_player_id
        # draw or not end yet
        return 0 if self.piece_num == self.board_shape[0] * self.board_shape[1] else -1

    def do_action(self, player_id, action):
        super().do_action(player_id, action)
        self.legal_actions.remove(action)

