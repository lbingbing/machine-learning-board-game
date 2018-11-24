#include <algorithm>

#include "gomoku_state.h"

GomokuState::GomokuState(int board_height, int board_width, int target, const std::string& state_compact_str, int player_id) : BlackWhiteState(board_height, board_width, state_compact_str, player_id), m_target(target) {
    for (int i = 0; i < m_board_height; ++i) {
        for (int j = 0; j < m_board_width; ++j) {
            if (m_board[i][j] == 0) {
                m_legal_actions.push_back({i, j});
            }
        }
    }
}

void GomokuState::reset() {
    BlackWhiteState::reset();
    m_legal_actions.clear();
    m_legal_actions.reserve(m_board_height * m_board_width);
    for (int i = 0; i < m_board_height; ++i) {
        for (int j = 0; j < m_board_width; ++j) {
            m_legal_actions.push_back({i, j});
        }
    }
}

const BlackWhiteState::Actions& GomokuState::get_legal_actions(int player_id) const {
    assert(m_last_player_id!=player_id);
    return m_legal_actions;
}

int GomokuState::get_result() const {
    if (m_last_action[0] == -1 && m_last_action[1] == -1) return -1;
    int i1, i2, j1, j2;
    // row
    j1 = m_last_action[1];
    while (j1-1 >= 0 && m_board[m_last_action[0]][j1-1]==m_last_player_id) --j1;
    j2 = m_last_action[1];
    while (j2+1 < m_board_width && m_board[m_last_action[0]][j2+1]==m_last_player_id) ++j2;
    if (j2-j1+1 >= m_target) return m_last_player_id;
    // column
    i1 = m_last_action[0];
    while (i1-1 >= 0 && m_board[i1-1][m_last_action[1]]==m_last_player_id) --i1;
    i2 = m_last_action[0];
    while (i2+1 < m_board_height && m_board[i2+1][m_last_action[1]]==m_last_player_id) ++i2;
    if (i2-i1+1 >= m_target) return m_last_player_id;
    // diagonal 1
    i1 = m_last_action[0];
    j1 = m_last_action[1];
    while (i1-1 >= 0 && j1-1 >= 0 && m_board[i1-1][j1-1]==m_last_player_id) {
        --i1;
        --j1;
    }
    i2 = m_last_action[0];
    j2 = m_last_action[1];
    while (i2+1 < m_board_height && j2+1 < m_board_width && m_board[i2+1][j2+1]==m_last_player_id) {
        ++i2;
        ++j2;
    }
    if (i2-i1+1 >= m_target) return m_last_player_id;
    // diagonal 2
    i1 = m_last_action[0];
    j1 = m_last_action[1];
    while (i1-1 >= 0 && j1+1 < m_board_width && m_board[i1-1][j1+1] == m_last_player_id) {
        --i1;
        ++j1;
    }
    i2 = m_last_action[0];
    j2 = m_last_action[1];
    while (i2+1 < m_board_height && j2-1 >= 0 && m_board[i2+1][j2-1] == m_last_player_id) {
        ++i2;
        --j2;
    }
    if (i2-i1+1 >= m_target) return m_last_player_id;
    // draw or not end yet
    return (m_piece_num == m_board_height * m_board_width) ? 0 : -1;
}

void GomokuState::do_action(int player_id, const Action& action) {
    BlackWhiteState::do_action(player_id, action);
    m_legal_actions.erase(std::remove(std::begin(m_legal_actions), std::end(m_legal_actions), action), std::end(m_legal_actions));
}

