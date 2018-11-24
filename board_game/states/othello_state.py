from .blackwhite_state import BlackWhiteState
from board_game.utils.utils import get_next_player_id

class OthelloState(BlackWhiteState):
    def __init__(self, board_shape):
        super().__init__(board_shape)
        assert(board_shape[0]%2==0 and board_shape[1]%2==0)

    def reset(self):
        super().reset()
        self.board[self.board_shape[0]//2-1][self.board_shape[1]//2-1] = 1
        self.board[self.board_shape[0]//2-1][self.board_shape[1]//2] = 2
        self.board[self.board_shape[0]//2][self.board_shape[1]//2-1] = 2
        self.board[self.board_shape[0]//2][self.board_shape[1]//2] = 1

    def get_target_pos(self, i, j, idir, jdir, player_id, opponent_player_id):
        assert(idir!=0 or jdir!=0)
        i1 = i + idir
        j1 = j + jdir
        while (idir == 0 or (idir < 0 and i1 > 0) or (idir > 0 and i1 < self.board_shape[0]-1)) and \
              (jdir == 0 or (jdir < 0 and j1 > 0) or (jdir > 0 and j1 < self.board_shape[1]-1)) and \
              self.board[i1][j1] == opponent_player_id:
            i1 += idir
            j1 += jdir
        if (idir == 0 or (idir < 0 and i1 >= 0 and i1 < i-1) or (idir > 0 and i1 <= self.board_shape[0]-1 and i1 > i+1)) and \
           (jdir == 0 or (jdir < 0 and j1 >= 0 and j1 < j-1) or (jdir > 0 and j1 <= self.board_shape[1]-1 and j1 > j+1)) and \
           self.board[i1][j1] == player_id:
            return i1, j1
        else:
            if idir == 0:
                pos_i = None
            else:
                pos_i = self.board_shape[0] if idir < 0 else -1
            if jdir == 0:
                pos_j = None
            else:
                pos_j = self.board_shape[1] if jdir < 0 else -1
            return pos_i, pos_j

    def get_legal_actions(self, player_id):
        super().get_legal_actions(player_id)
        opponent_player_id = get_next_player_id(player_id)
        legal_actions = []
        for i in range(self.board_shape[0]):
            for j in range(self.board_shape[1]):
                if self.board[i][j] == 0:
                    if self.get_target_pos(i, j, -1, 0, player_id, opponent_player_id)[0] < i-1 or \
                       self.get_target_pos(i, j, 1, 0, player_id, opponent_player_id)[0] > i+1 or \
                       self.get_target_pos(i, j, 0, -1, player_id, opponent_player_id)[1] < j-1 or \
                       self.get_target_pos(i, j, 0, 1, player_id, opponent_player_id)[1] > j+1 or \
                       self.get_target_pos(i, j, -1, -1, player_id, opponent_player_id)[0] < i-1 or \
                       self.get_target_pos(i, j, -1, 1, player_id, opponent_player_id)[0] < i-1 or \
                       self.get_target_pos(i, j, 1, -1, player_id, opponent_player_id)[0] > i+1 or \
                       self.get_target_pos(i, j, 1, 1, player_id, opponent_player_id)[0] > i+1:
                        legal_actions.append((i, j))
        return legal_actions

    def get_result(self):
        if self.last_action == None:
            return -1
        if self.get_legal_actions(get_next_player_id(self.last_player_id)):
            return -1
        black_num = sum(1 for e in self.board for v in e if v == 1)
        white_num = sum(1 for e in self.board for v in e if v == 2)
        if black_num > white_num:
            return 1
        if black_num < white_num:
            return 2
        else:
            return 0

    def change_color(self, i, j, idir, jdir, player_id, opponent_player_id):
        assert(idir!=0 or jdir!=0)
        target = self.get_target_pos(i, j, idir, jdir, player_id, opponent_player_id)
        i1 = target[0] - idir if idir != 0 else i
        j1 = target[1] - jdir if jdir != 0 else j
        while (idir == 0 or (idir < 0 and i1 < i) or (idir > 0 and i1 > i)) and \
              (jdir == 0 or (jdir < 0 and j1 < j) or (jdir > 0 and j1 > j)):
            self.board[i1][j1] = player_id
            i1 -= idir
            j1 -= jdir

    def do_action(self, player_id, action):
        super().do_action(player_id, action)
        opponent_player_id = get_next_player_id(player_id)
        i, j = action
        self.change_color(i, j, -1,  0, player_id, opponent_player_id)
        self.change_color(i, j,  1,  0, player_id, opponent_player_id)
        self.change_color(i, j,  0, -1, player_id, opponent_player_id)
        self.change_color(i, j,  0,  1, player_id, opponent_player_id)
        self.change_color(i, j, -1, -1, player_id, opponent_player_id)
        self.change_color(i, j, -1,  1, player_id, opponent_player_id)
        self.change_color(i, j,  1, -1, player_id, opponent_player_id)
        self.change_color(i, j,  1,  1, player_id, opponent_player_id)

