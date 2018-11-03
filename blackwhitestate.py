import numpy as np

from utils import get_next_player_id

class BlackWhiteState:
    def __init__(self, board_shape):
        self.board_shape = board_shape
        self.reset()

    def reset(self):
        self.board = [[0 for j in range(self.board_shape[1])] for i in range(self.board_shape[0])]
        self.last_player_id = 2
        self.last_action = None
        self.piece_num = 0
        self.legal_actions = set((i, j) for i in range(self.board_shape[0]) for j in range(self.board_shape[1]))

    def copy(self, rhs):
        self.board_shape = rhs.board_shape
        self.board = list(list(e) for e in rhs.board)
        self.last_player_id = rhs.last_player_id
        self.last_action = rhs.last_action
        self.piece_num = rhs.piece_num
        self.legal_actions = set(rhs.legal_actions)

    def __str__(self):
        return '\n\n'.join(map(lambda row: '  '.join(map(str, row)), self.board)).replace('0', '-')

    def compact_str(self):
        return ''.join(map(lambda row: ''.join(map(str, row)), self.board))

    def cmd_strs(self):
        return ['release/blackwhite_mcts_get_action.exe', str(self.board_shape[0]), str(self.board_shape[1]), self.compact_str(), str(self.get_cur_player_id())]

    def get_cur_player_id(self):
        return get_next_player_id(self.last_player_id)

    def get_legal_actions(self, player_id):
        assert(self.last_player_id!=player_id)
        return tuple(self.legal_actions)

    def is_end(self):
        return self.get_result() >= 0

    def get_result(self):
        '''
        return result:
            -1 when if game dones't end
            0 when if it is draw
            n when player n wins
        '''
        pass

    def do_action(self, player_id, action):
        assert(self.last_player_id!=player_id)
        assert(self.board[action[0]][action[1]]==0)
        self.board[action[0]][action[1]] = player_id
        self.last_player_id = player_id
        self.last_action = action
        self.piece_num += 1
        self.legal_actions.remove(action)

    def to_state_m(self):
        res = 3 - np.array(self.board).reshape(-1) * 2
        res = np.where(res==3, 0, res)
        res = np.stack((res, np.full_like(res, 1 if self.last_player_id==2 else -1)), axis = 1)
        return res.reshape(1, self.board_shape[0], self.board_shape[1], 2)

    def get_action_dim(self):
        return self.board_shape[0] * self.board_shape[1]

    def action_to_action_index(self, action):
        return action[0] * self.board_shape[1] + action[1]

    def action_index_to_action(self, action_index):
        return (action_index // self.board_shape[0], action_index % self.board_shape[1])

    def get_legal_action_mask_m(self):
        legal_action_mask_m = np.zeros((1, self.get_action_dim()))
        legal_action_indexes = [self.action_to_action_index(action) for action in self.get_legal_actions(self.get_cur_player_id())]
        legal_action_mask_m[:, legal_action_indexes] = 1
        return legal_action_mask_m

    @staticmethod
    def get_equivalents(m):
        m_l = [m]
        m_l.append(np.rot90(m, axes = (1, 2)))
        m_l.append(np.rot90(m, k = 2, axes = (1, 2)))
        m_l.append(np.rot90(m, k = 3, axes = (1, 2)))
        m_l.append(np.flip(m, axis = 1))
        m_l.append(np.rot90(np.flip(m, axis = 1), axes = (1, 2)))
        m_l.append(np.rot90(np.flip(m, axis = 1), k = 2, axes = (1, 2)))
        m_l.append(np.rot90(np.flip(m, axis = 1), k = 3, axes = (1, 2)))
        return m_l

    @staticmethod
    def get_equivalent_state_m_batch(state_m):
        state_m_l = BlackWhiteState.get_equivalents(state_m)
        return np.concatenate(state_m_l, axis = 0)

    @staticmethod
    def get_equivalent_Ps_m_batch(Ps_m, board_shape):
        Ps_m = Ps_m.reshape(Ps_m.shape[0], board_shape[0], board_shape[1])
        Ps_m_l = BlackWhiteState.get_equivalents(Ps_m)
        Ps_m_l = [m.reshape(m.shape[0], -1) for m in Ps_m_l]
        return np.concatenate(Ps_m_l, axis = 0)

    @staticmethod
    def get_equivalent_V_m_batch(V_m):
        return np.tile(V_m, (8, 1))

class TicTacToeState(BlackWhiteState):
    def __init__(self, board_shape):
        super().__init__(board_shape)
        assert(board_shape[0]==board_shape[1])

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

class GomokuState(BlackWhiteState):
    def __init__(self, board_shape, target = 5):
        super().__init__(board_shape)

        self.target = target

    def copy(self, rhs):
        super().copy(rhs)
        self.target = rhs.target

    def cmd_strs(self):
        return super().cmd_strs() + [str(self.target)]

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

