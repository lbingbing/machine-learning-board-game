#include <algorithm>
#include <iterator>
#include <cassert>
#include <sstream>

#include "blackwhite_state.h"
#include "utils.h"

BlackWhiteState::BlackWhiteState(int board_height, int board_width, const std::string& state_compact_str, int player_id) : m_board_height(board_height), m_board_width(board_width), m_board(board_height, std::vector<int>(board_width)), m_last_player_id(get_next_player_id(player_id)), m_last_action{-1, -1}, m_piece_num(board_height*board_width), m_legal_actions{} {
    assert(board_height * board_width == state_compact_str.size());
    int index = 0;
    for (int i = 0; i < m_board_height; ++i) {
        for (int j = 0; j < m_board_width; ++j) {
            int p = state_compact_str[index++] - '0';
            m_board[i][j] = p;
            if (p == 0) {
                --m_piece_num;
                m_legal_actions.push_back({i, j});
            }
        }
    }
}

void BlackWhiteState::reset() {
    for (int i = 0; i < m_board_height; ++i) {
        for (int j = 0; j < m_board_width; ++j) {
            m_board[i][j] = 0;
        }
    }
    m_last_player_id = -1;
    m_last_action = {-1, -1};
    m_piece_num = 0;
    m_legal_actions.clear();
    m_legal_actions.reserve(m_board_height * m_board_width);
    for (int i = 0; i < m_board_height; ++i) {
        for (int j = 0; j < m_board_width; ++j) {
            m_legal_actions.push_back({i, j});
        }
    }
}

std::string BlackWhiteState::to_compact_string() const {
    std::ostringstream oss;
    for (int i = 0; i < m_board_height; ++i) {
        for (int j = 0; j < m_board_width; ++j) {
            oss << m_board[i][j];
        }
    }
    return oss.str();
}

std::string BlackWhiteState::to_string() const {
    std::ostringstream oss;
    for (int i = 0; i < m_board_height; ++i) {
        for (int j = 0; j < m_board_width; ++j) {
            oss << m_board[i][j];
            if (j != m_board_width-1) oss << "  ";
        }
        if (i != m_board_height-1) oss << "\n\n";
    }
    return oss.str();
}

void BlackWhiteState::do_action(int player_id, const Action& action) {
    assert(m_board[action[0]][action[1]]==0);
    m_board[action[0]][action[1]] = player_id;
    m_last_player_id = player_id;
    m_last_action = action;
    ++m_piece_num;
    m_legal_actions.erase(std::remove(std::begin(m_legal_actions), std::end(m_legal_actions), action), std::end(m_legal_actions));
}

