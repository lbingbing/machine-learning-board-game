#include "othello_state.h"
#include "utils.h"

OthelloState::OthelloState(int board_height, int board_width) : BlackWhiteState(board_height, board_width) {
    assert(board_width%2==0 && board_height%2==0);
    reset_self();
}

void OthelloState::reset() {
    BlackWhiteState::reset();
    reset_self();
}

void OthelloState::reset_self() {
    m_board[m_board_height/2-1][m_board_width/2-1] = 1;
    m_board[m_board_height/2-1][m_board_width/2] = 2;
    m_board[m_board_height/2][m_board_width/2-1] = 2;
    m_board[m_board_height/2][m_board_width/2] = 1;
}

OthelloState::TargetPos OthelloState::get_target_pos(int i, int j, int idir, int jdir, int player_id, int opponent_player_id) const {
    assert(idir!=0 || jdir!=0);
    int i1;
    int j1;
    i1 = i + idir;
    j1 = j + jdir;
    while ((idir == 0 || (idir < 0 && i1 > 0) || (idir > 0 && i1 < m_board_height-1)) &&
           (jdir == 0 || (jdir < 0 && j1 > 0) || (jdir > 0 && j1 < m_board_width-1)) &&
           m_board[i1][j1] == opponent_player_id) {
        i1 += idir;
        j1 += jdir;
    }
    if ((idir == 0 || (idir < 0 && i1 >= 0 && i1 < i-1) || (idir > 0 && i1 <= m_board_height-1 && i1 > i+1)) &&
        (jdir == 0 || (jdir < 0 && j1 >= 0 && j1 < j-1) || (jdir > 0 && j1 <= m_board_width-1 && j1 > j+1)) &&
        m_board[i1][j1] == player_id) {
        return {i1, j1};
    } else {
        int pos_i;
        int pos_j;
        if (idir == 0) pos_i = -1;
        else           pos_i = idir < 0 ? m_board_height : -1;
        if (jdir == 0) pos_j = -1;
        else           pos_j = jdir < 0 ? m_board_width : -1;
        return {pos_i, pos_j};
    }
}

BlackWhiteState::Actions OthelloState::get_legal_actions(int player_id) const {
    assert(m_last_player_id!=player_id);
    int opponent_player_id = get_next_player_id(player_id);
    Actions legal_actions;
    for (int i = 0; i < m_board_height; ++i) {
        for (int j = 0; j < m_board_width; ++j) {
            if (m_board[i][j] == 0) {
                if (get_target_pos(i, j, -1,  0, player_id, opponent_player_id)[0] < i-1 ||
                    get_target_pos(i, j,  1,  0, player_id, opponent_player_id)[0] > i+1 ||
                    get_target_pos(i, j,  0, -1, player_id, opponent_player_id)[1] < j-1 ||
                    get_target_pos(i, j,  0,  1, player_id, opponent_player_id)[1] > j+1 ||
                    get_target_pos(i, j, -1, -1, player_id, opponent_player_id)[0] < i-1 ||
                    get_target_pos(i, j, -1,  1, player_id, opponent_player_id)[0] < i-1 ||
                    get_target_pos(i, j,  1, -1, player_id, opponent_player_id)[0] > i+1 ||
                    get_target_pos(i, j,  1,  1, player_id, opponent_player_id)[0] > i+1) {
                    legal_actions.push_back({i, j});
                }
            }
        }
    }
    return legal_actions;
}

int OthelloState::get_result() const {
    if (m_last_action[0] == -1 && m_last_action[1] == -1) return -1;
    if (!get_legal_actions(get_next_player_id(m_last_player_id)).empty()) return -1;
    int black_num = 0;
    int white_num = 0;
    for (int i = 0; i < m_board_height; ++i) {
        for (int j = 0; j < m_board_width; ++j) {
            if (m_board[i][j] == 1) {
                ++black_num;
            }else if (m_board[i][j] == 2) {
                ++white_num;
            }
        }
    }
    if      (black_num > white_num) return 1;
    else if (black_num < white_num) return 2;
    else                            return 0;
}

void OthelloState::change_color(int i, int j, int idir, int jdir, int player_id, int opponent_player_id) {
    assert(idir!=0 || jdir!=0);
    TargetPos target = get_target_pos(i, j, idir, jdir, player_id, opponent_player_id);
    int i1 = idir != 0 ? target[0] - idir : i;
    int j1 = jdir != 0 ? target[1] - jdir : j;
    while ((idir == 0 || (idir < 0 && i1 < i) || (idir > 0 && i1 > i)) &&
           (jdir == 0 || (jdir < 0 && j1 < j) || (jdir > 0 && j1 > j))) {
        m_board[i1][j1] = player_id;
        i1 -= idir;
        j1 -= jdir;
    }
}    

void OthelloState::do_action(int player_id, const Action& action) {
    BlackWhiteState::do_action(player_id, action);
    int opponent_player_id = get_next_player_id(player_id);
    int i = action[0];
    int j = action[1];
    change_color(i, j, -1,  0, player_id, opponent_player_id);
    change_color(i, j,  1,  0, player_id, opponent_player_id);
    change_color(i, j,  0, -1, player_id, opponent_player_id);
    change_color(i, j,  0,  1, player_id, opponent_player_id);
    change_color(i, j, -1, -1, player_id, opponent_player_id);
    change_color(i, j, -1,  1, player_id, opponent_player_id);
    change_color(i, j,  1, -1, player_id, opponent_player_id);
    change_color(i, j,  1,  1, player_id, opponent_player_id);
}

