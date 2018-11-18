import numpy as np

from board_game.utils.utils import get_next_player_id

#    0   1   2   3   4   5   6   7   8
#  0 +---+---+---+---+---+---+---+---+
#    |   |   |   | \ | / |   |   |   |
#  1 +---+---+---+---+---+---+---+---+
#    |   |   |   | / | \ |   |   |   |
#  2 +---x---+---+---+---+---+---x---+
#    |   |   |   |   |   |   |   |   |
#  3 +---+---+---+---+---+---+---+---+
#    |   |   |   |   |   |   |   |   |
#  4 +---+---+---+---+---+---+---+---+
#    |                               |
#  5 +---+---+---+---+---+---+---+---+
#    |   |   |   |   |   |   |   |   |
#  6 +---+---+---+---+---+---+---+---+
#    |   |   |   |   |   |   |   |   |
#  7 +---x---+---+---+---+---+---x---+
#    |   |   |   | \ | / |   |   |   |
#  8 +---+---+---+---+---+---+---+---+
#    |   |   |   | / | \ |   |   |   |
#  9 +---+---+---+---+---+---+---+---+

BOARD_WIDTH = 9
BOARD_HEIGHT = 10

MAX_ACTION_PER_GAME = 200

NULL = 0
R_JIANG = 1
R_SHI   = 2
R_XIANG = 3
R_BING  = 4
R_PAO   = 5
R_MA    = 6
R_JU    = 7
B_JIANG = -1
B_SHI   = -2
B_XIANG = -3
B_BING  = -4
B_PAO   = -5
B_MA    = -6
B_JU    = -7

def piece_value_to_player_id(piece_value):
    if piece_value > NULL:
        return 1
    elif piece_value < NULL:
        return 2
    else:
        return 0

def piece_value_to_name(piece_value):
    if piece_value == R_JIANG or piece_value == B_JIANG:
        return 'Jiang'
    if piece_value == R_SHI or piece_value == B_SHI:
        return 'Shi'
    if piece_value == R_XIANG or piece_value == B_XIANG:
        return 'Xiang'
    if piece_value == R_BING or piece_value == B_BING:
        return 'Bing'
    if piece_value == R_PAO or piece_value == B_PAO:
        return 'Pao'
    if piece_value == R_MA or piece_value == B_MA:
        return 'Ma'
    if piece_value == R_JU or piece_value == B_JU:
        return 'Ju'
    assert(0)

def get_action_and_action_index_mapping():
    action_to_action_index = {}
    index = 0
    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            # SHI
            if (i, j) in ((0, 3), (0, 5), (1, 4), (2, 3), (2, 5), (7, 3), (7, 5), (8, 4), (9, 3), (9, 5)):
                if (i <= 2 and i-1 >= 0 or i >= 7 and i-1 >= 7) and j-1 >= 3:
                    action_to_action_index[(i, j, i-1, j-1)] = index
                    index += 1
                if (i <= 2 and i-1 >= 0 or i >= 7 and i-1 >= 7) and j+1 <= 5:
                    action_to_action_index[(i, j, i-1, j+1)] = index
                    index += 1
                if (i <= 2 and i+1 <= 2 or i >= 7 and i+1 < BOARD_HEIGHT) and j-1 >= 3:
                    action_to_action_index[(i, j, i+1, j-1)] = index
                    index += 1
                if (i <= 2 and i+1 <= 2 or i >= 7 and i+1 < BOARD_HEIGHT) and j+1 <= 5:
                    action_to_action_index[(i, j, i+1, j+1)] = index
                    index += 1
            # XIANG
            if (i, j) in ((0, 2), (0, 6), (2, 0), (2, 4), (2, 8), (4, 2), (4, 6), (5, 2), (5, 6), (7, 0), (7, 4), (7, 8), (9, 2), (9, 6)):
                if (i <= 4 and i-2 >= 0 or i >= 5 and i-2 >= 5) and j-2 >= 0:
                    action_to_action_index[(i, j, i-2, j-2)] = index
                    index += 1
                if (i <= 4 and i-2 >= 0 or i >= 5 and i-2 >= 5) and j+2 < BOARD_WIDTH:
                    action_to_action_index[(i, j, i-2, j+2)] = index
                    index += 1
                if (i <= 4 and i+2 <= 4 or i >= 5 and i+2 < BOARD_HEIGHT) and j-2 >= 0:
                    action_to_action_index[(i, j, i+2, j-2)] = index
                    index += 1
                if (i <= 4 and i+2 <= 4 or i >= 5 and i+2 < BOARD_HEIGHT) and j+2 < BOARD_WIDTH:
                    action_to_action_index[(i, j, i+2, j+2)] = index
                    index += 1
            # MA
            if i-2 >= 0 and j-1 >= 0:
                action_to_action_index[(i, j, i-2, j-1)] = index
                index += 1
            if i-2 >= 0 and j+1 < BOARD_WIDTH:
                action_to_action_index[(i, j, i-2, j+1)] = index
                index += 1
            if i-1 >= 0 and j-2 >= 0:
                action_to_action_index[(i, j, i-1, j-2)] = index
                index += 1
            if i-1 >= 0 and j+2 < BOARD_WIDTH:
                action_to_action_index[(i, j, i-1, j+2)] = index
                index += 1
            if i+1 < BOARD_HEIGHT and j-2 >= 0:
                action_to_action_index[(i, j, i+1, j-2)] = index
                index += 1
            if i+1 < BOARD_HEIGHT and j+2 < BOARD_WIDTH:
                action_to_action_index[(i, j, i+1, j+2)] = index
                index += 1
            if i+2 < BOARD_HEIGHT and j-1 >= 0:
                action_to_action_index[(i, j, i+2, j-1)] = index
                index += 1
            if i+2 < BOARD_HEIGHT and j+1 < BOARD_WIDTH:
                action_to_action_index[(i, j, i+2, j+1)] = index
                index += 1
            # JU
            for j1 in range(BOARD_WIDTH):
                if j1 != j:
                    action_to_action_index[(i, j, i, j1)] = index
                    index += 1
            for i1 in range(BOARD_HEIGHT):
                if i1 != i:
                    action_to_action_index[(i, j, i1, j)] = index
                    index += 1

    action_index_to_action = {index : action for action, index in action_to_action_index.items()}

    action_index_pairs = []
    for action, action_index in action_to_action_index.items():
        equivalent_action = (action[0], BOARD_WIDTH-1-action[1], action[2], BOARD_WIDTH-1-action[3])
        equivalent_action_index = action_to_action_index[equivalent_action]
        action_index_pairs.append((action_index, equivalent_action_index))
    action_index_pairs.sort()
    action_index_to_equivalent_action_index = [equivalent_action_index for action_index, equivalent_action_index in action_index_pairs]

    return action_to_action_index, action_index_to_action, action_index_to_equivalent_action_index

action_to_action_index_table, action_index_to_action_table, action_index_to_equivalent_action_index_table = get_action_and_action_index_mapping()
ACTION_DIM = len(action_to_action_index_table)

def append_legal_action_JIANG(legal_actions, board, i, j, player_id, sign):
    if (player_id == 1 and i-1 >= 7 or player_id == 2 and i-1 >= 0) and board[i-1][j]*sign <= NULL:
        legal_actions.append((i, j, i-1, j))
    if (player_id == 1 and i+1 < BOARD_HEIGHT or player_id == 2 and i+1 <= 2) and board[i+1][j]*sign <= NULL:
        legal_actions.append((i, j, i+1, j))
    if j-1 >= 3 and board[i][j-1]*sign <= NULL:
        legal_actions.append((i, j, i, j-1))
    if j+1 <= 5 and board[i][j+1]*sign <= NULL:
        legal_actions.append((i, j, i, j+1))
    if player_id == 1:
        i1 = 0
        while i1 <= 2 and board[i1][j] != B_JIANG:
            i1 += 1
        if i1 <= 2:
            i2 = i1+1
            while i2 != i and board[i2][j] == NULL:
                i2 += 1
            if i2 == i:
                legal_actions.append((i, j, i1, j))
    else:
        i1 = BOARD_HEIGHT-1
        while i1 >= 7 and board[i1][j] != R_JIANG:
            i1 -= 1
        if i1 >= 7:
            i2 = i1-1
            while i2 != i and board[i2][j] == NULL:
                i2 -= 1
            if i2 == i:
                legal_actions.append((i, j, i1, j))

def append_legal_action_SHI(legal_actions, board, i, j, player_id, sign):
    if player_id == 1 and i-1 >= 7 or player_id == 2 and i-1 >= 0:
        if j-1 >= 3 and board[i-1][j-1]*sign <= NULL:
            legal_actions.append((i, j, i-1, j-1))
        if j+1 <= 5 and board[i-1][j+1]*sign <= NULL:
            legal_actions.append((i, j, i-1, j+1))
    if player_id == 1 and i+1 < BOARD_HEIGHT or player_id == 2 and i+1 <= 2:
        if j-1 >= 3 and board[i+1][j-1]*sign <= NULL:
            legal_actions.append((i, j, i+1, j-1))
        if j+1 <= 5 and board[i+1][j+1]*sign <= NULL:
            legal_actions.append((i, j, i+1, j+1))

def append_legal_action_XIANG(legal_actions, board, i, j, player_id, sign):
    if player_id == 1 and i-2 >= 5 or player_id == 2 and i-2 >= 0:
        if j-2 >= 0 and board[i-1][j-1] == NULL and board[i-2][j-2]*sign <= NULL:
            legal_actions.append((i, j, i-2, j-2))
        if j+2 < BOARD_WIDTH and board[i-1][j+1] == NULL and board[i-2][j+2]*sign <= NULL:
            legal_actions.append((i, j, i-2, j+2))
    if player_id == 1 and i+2 < BOARD_HEIGHT or player_id == 2 and i+2 <= 4:
        if j-2 >= 0 and board[i+1][j-1] == NULL and board[i+2][j-2]*sign <= NULL:
            legal_actions.append((i, j, i+2, j-2))
        if j+2 < BOARD_WIDTH and board[i+1][j+1] == NULL and board[i+2][j+2]*sign <= NULL:
            legal_actions.append((i, j, i+2, j+2))

def append_legal_action_BING(legal_actions, board, i, j, player_id, sign):
    if (player_id == 1 and i-1 >=0 or player_id == 2 and i+1 < BOARD_HEIGHT) and board[i-sign][j]*sign <= NULL:
        legal_actions.append((i, j, i-sign, j))
    if player_id == 1 and i <= 4 or player_id == 2 and i >= 5:
        if j-1 >= 0 and board[i][j-1]*sign <= NULL:
            legal_actions.append((i, j, i, j-1))
        if j+1 < BOARD_WIDTH and board[i][j+1]*sign <= NULL:
            legal_actions.append((i, j, i, j+1))

def append_legal_action_PAO(legal_actions, board, i, j, sign):
    # up
    i1 = i-1
    while i1 >= 0 and board[i1][j] == NULL:
        legal_actions.append((i, j, i1, j))
        i1 -= 1
    i1 -= 1
    while i1 >= 0 and board[i1][j] == NULL:
        i1 -= 1
    if i1 >= 0 and board[i1][j]*sign <= NULL:
        legal_actions.append((i, j, i1, j))
    # down
    i1 = i+1
    while i1 < BOARD_HEIGHT and board[i1][j] == NULL:
        legal_actions.append((i, j, i1, j))
        i1 += 1
    i1 += 1
    while i1 < BOARD_HEIGHT and board[i1][j] == NULL:
        i1 += 1
    if i1 < BOARD_HEIGHT and board[i1][j]*sign <= NULL:
        legal_actions.append((i, j, i1, j))
    # left
    j1 = j-1
    while j1 >= 0 and board[i][j1] == NULL:
        legal_actions.append((i, j, i, j1))
        j1 -= 1
    j1 -= 1
    while j1 >= 0 and board[i][j1] == NULL:
        j1 -= 1
    if j1 >= 0 and board[i][j1]*sign <= NULL:
        legal_actions.append((i, j, i, j1))
    # right
    j1 = j+1
    while j1 < BOARD_WIDTH and board[i][j1] == NULL:
        legal_actions.append((i, j, i, j1))
        j1 += 1
    j1 += 1
    while j1 < BOARD_WIDTH and board[i][j1] == NULL:
        j1 += 1
    if j1 < BOARD_WIDTH and board[i][j1]*sign <= NULL:
        legal_actions.append((i, j, i, j1))

def append_legal_action_MA(legal_actions, board, i, j, sign):
    if i-2 >= 0 and board[i-1][j] == NULL:
        if j-1 >= 0 and board[i-2][j-1]*sign <= NULL:
            legal_actions.append((i, j, i-2, j-1))
        if j+1 < BOARD_WIDTH and board[i-2][j+1]*sign <= NULL:
            legal_actions.append((i, j, i-2, j+1))
    if i+2 < BOARD_HEIGHT and board[i+1][j] == NULL:
        if j-1 >= 0 and board[i+2][j-1]*sign <= NULL:
            legal_actions.append((i, j, i+2, j-1))
        if j+1 < BOARD_WIDTH and board[i+2][j+1]*sign <= NULL:
            legal_actions.append((i, j, i+2, j+1))
    if j-2 >= 0 and board[i][j-1] == NULL:
        if i-1 >= 0 and board[i-1][j-2]*sign <= NULL:
            legal_actions.append((i, j, i-1, j-2))
        if i+1 < BOARD_HEIGHT and board[i+1][j-2]*sign <= NULL:
            legal_actions.append((i, j, i+1, j-2))
    if j+2 < BOARD_WIDTH and board[i][j+1] == NULL:
        if i-1 >= 0 and board[i-1][j+2]*sign <= NULL:
            legal_actions.append((i, j, i-1, j+2))
        if i+1 < BOARD_HEIGHT and board[i+1][j+2]*sign <= NULL:
            legal_actions.append((i, j, i+1, j+2))

def append_legal_action_JU(legal_actions, board, i, j, sign):
    # up
    i1 = i-1
    while i1 >= 0:
        if board[i1][j]*sign <= NULL:
            legal_actions.append((i, j, i1, j))
        if board[i1][j]*sign != NULL:
            break
        i1 -= 1
    # down
    i1 = i+1
    while i1 < BOARD_HEIGHT:
        if board[i1][j]*sign <= NULL:
            legal_actions.append((i, j, i1, j))
        if board[i1][j]*sign != NULL:
            break
        i1 += 1
    # left
    j1 = j-1
    while j1 >= 0:
        if board[i][j1]*sign <= NULL:
            legal_actions.append((i, j, i, j1))
        if board[i][j1]*sign != NULL:
            break
        j1 -= 1
    # right
    j1 = j+1
    while j1 < BOARD_WIDTH:
        if board[i][j1]*sign <= NULL:
            legal_actions.append((i, j, i, j1))
        if board[i][j1]*sign != NULL:
            break
        j1 += 1

class ChessState:
    def __init__(self):
        self.board_shape = (BOARD_HEIGHT, BOARD_WIDTH)
        self.reset()

    def reset(self):
        self.board = [
                [B_JU  , B_MA , B_XIANG, B_SHI, B_JIANG, B_SHI, B_XIANG, B_MA , B_JU  ],
                [NULL  , NULL , NULL   , NULL , NULL   , NULL , NULL   , NULL , NULL  ],
                [NULL  , B_PAO, NULL   , NULL , NULL   , NULL , NULL   , B_PAO, NULL  ],
                [B_BING, NULL , B_BING , NULL , B_BING , NULL , B_BING , NULL , B_BING],
                [NULL  , NULL , NULL   , NULL , NULL   , NULL , NULL   , NULL , NULL  ],
                [NULL  , NULL , NULL   , NULL , NULL   , NULL , NULL   , NULL , NULL  ],
                [R_BING, NULL , R_BING , NULL , R_BING , NULL , R_BING , NULL , R_BING],
                [NULL  , R_PAO, NULL   , NULL , NULL   , NULL , NULL   , R_PAO, NULL  ],
                [NULL  , NULL , NULL   , NULL , NULL   , NULL , NULL   , NULL , NULL  ],
                [R_JU  , R_MA , R_XIANG, R_SHI, R_JIANG, R_SHI, R_XIANG, R_MA , R_JU  ],
            ]
        #self.board = [
        #        [NULL, NULL, NULL   , B_SHI, B_JIANG, B_SHI  , B_XIANG, NULL , NULL],
        #        [NULL, NULL, NULL   , NULL , NULL   , NULL   , NULL   , NULL , NULL],
        #        [NULL, NULL, NULL   , NULL , B_XIANG, NULL   , NULL   , NULL , NULL],
        #        [NULL, NULL, NULL   , NULL , NULL   , NULL   , NULL   , NULL , NULL],
        #        [NULL, NULL, NULL   , NULL , NULL   , NULL   , NULL   , NULL , NULL],
        #        [NULL, NULL, NULL   , NULL , NULL   , NULL   , NULL   , NULL , NULL],
        #        [NULL, NULL, NULL   , NULL , NULL   , NULL   , NULL   , NULL , NULL],
        #        [NULL, NULL, NULL   , NULL , R_XIANG, NULL   , NULL   , NULL , NULL],
        #        [NULL, NULL, NULL   , NULL , R_SHI  , NULL   , NULL   , R_PAO, NULL],
        #        [NULL, NULL, R_XIANG, R_SHI, NULL   , R_JIANG, NULL   , R_PAO, NULL],
        #    ]
        self.left_action_num = MAX_ACTION_PER_GAME
        self.cur_player_id = 1

    def copy(self, rhs):
        self.board = list(list(e) for e in rhs.board)
        self.left_action_num = rhs.left_action_num
        self.cur_player_id = rhs.cur_player_id

    def __str__(self):
        return '\n\n'.join(map(lambda row: '  '.join(map('{0:2d}'.format, row)), self.board)).replace('0', '-')

    def compact_str(self):
        return ''.join(map(lambda row: ''.join(map(str, row)), self.board))

    def get_cur_player_id(self):
        return self.cur_player_id

    def get_board(self):
        return self.board

    def get_legal_actions(self, player_id):
        assert(self.cur_player_id==player_id)
        legal_actions = []
        sign = 1 if player_id == 1 else -1
        for i in range(BOARD_HEIGHT):
            for j in range(BOARD_WIDTH):
                p = self.board[i][j]
                if p == R_JIANG*sign:
                    append_legal_action_JIANG(legal_actions, self.board, i, j, self.cur_player_id, sign)
                elif p == R_SHI*sign:
                    append_legal_action_SHI(legal_actions, self.board, i, j, self.cur_player_id, sign)
                elif p == R_XIANG*sign:
                    append_legal_action_XIANG(legal_actions, self.board, i, j, self.cur_player_id, sign)
                elif p == R_BING*sign:
                    append_legal_action_BING(legal_actions, self.board, i, j, self.cur_player_id, sign)
                elif p == R_PAO*sign:
                    append_legal_action_PAO(legal_actions, self.board, i, j, sign)
                elif p == R_MA*sign:
                    append_legal_action_MA(legal_actions, self.board, i, j, sign)
                elif p == R_JU*sign:
                    append_legal_action_JU(legal_actions, self.board, i, j, sign)
        for i0, j0, i1, j1 in legal_actions:
            if self.cur_player_id == 1 and self.board[i1][j1] == B_JIANG or \
               self.cur_player_id == 2 and self.board[i1][j1] == R_JIANG:
                   return [(i0, j0, i1, j1)]

        return legal_actions

    def is_end(self):
        return self.get_result() >= 0

    def get_result(self):
        '''
        return result:
            -1 when if game dones't end
            0 when if it is draw
            n when player n wins
        '''
        if self.cur_player_id == 1:
            if not any(self.board[i][j]==R_JIANG for i in (7, 8, 9) for j in (3, 4, 5)):
                return 2
        else:
            if not any(self.board[i][j]==B_JIANG for i in (0, 1, 2) for j in (3, 4, 5)):
                return 1
        return 0 if self.left_action_num == 0 else -1

    def do_action(self, player_id, action):
        assert(self.cur_player_id==player_id)
        assert(player_id==1 and self.board[action[0]][action[1]]>NULL or
               player_id==2 and self.board[action[0]][action[1]]<NULL)
        assert(player_id==1 and self.board[action[2]][action[3]]<=NULL or
               player_id==2 and self.board[action[2]][action[3]]>=NULL)
        self.board[action[2]][action[3]] = self.board[action[0]][action[1]]
        self.board[action[0]][action[1]] = NULL
        self.left_action_num -= 1
        self.cur_player_id = get_next_player_id(player_id)

    def to_state_m(self):
        res = np.array(self.board).reshape(-1) / 7
        res = np.stack((res, np.full_like(res, 1 if self.cur_player_id==1 else -1)), axis = 1)
        return res.reshape(1, BOARD_HEIGHT, BOARD_WIDTH, 2)

    def get_action_dim(self):
        return ACTION_DIM

    def action_to_action_index(self, action):
        return action_to_action_index_table[action]

    def action_index_to_action(self, action_index):
        return action_index_to_action_table[action_index]

    def get_legal_action_mask_m(self):
        legal_action_mask_m = np.zeros((1, self.get_action_dim()))
        legal_action_indexes = [self.action_to_action_index(action) for action in self.get_legal_actions(self.cur_player_id)]
        legal_action_mask_m[:, legal_action_indexes] = 1
        return legal_action_mask_m

    @staticmethod
    def get_equivalent_state_m_batch(state_m):
        state_m_l = [state_m]
        state_m_l.append(np.flip(state_m, axis = 2))
        state_m_l = [m.reshape(m.shape[0], BOARD_HEIGHT, BOARD_WIDTH, 2) for m in state_m_l]
        return np.concatenate(state_m_l)

    @staticmethod
    def get_equivalent_Ps_m_batch(Ps_m, board_shape):
        Ps_m_l = [Ps_m]

        Ps_m1 = np.empty_like(Ps_m)
        Ps_m1[:,action_index_to_equivalent_action_index_table] = Ps_m[:,list(range(ACTION_DIM))]
        Ps_m_l.append(Ps_m1)

        return np.concatenate(Ps_m_l)

    @staticmethod
    def get_equivalent_V_m_batch(V_m):
        return np.tile(V_m, (2, 1))
        return V_m

