#include <algorithm>
#include <iterator>
#include <cassert>
#include <sstream>

#include "ChessState.h"

ChessState::ChessState(const std::string& state_compact_str, int player_id, int left_action_num) : m_cur_player_id(player_id), m_left_action_num(left_action_num) {
    int index = 0;
    for (int i = 0; i < BOARD_HEIGHT; ++i) {
        for (int j = 0; j < BOARD_WIDTH; ++j) {
            int sign = 1;
            if (state_compact_str[index] == '-') {
                sign = -1;
                ++index;
            }
            int p = (state_compact_str[index++] - '0') * sign;
            m_board[i][j] = p;
        }
    }
}

void ChessState::reset() {
    m_board = {B_JU  , B_MA , B_XIANG, B_SHI, B_JIANG, B_SHI, B_XIANG, B_MA , B_JU  ,
               NUL   , NUL  , NUL    , NUL  , NUL    , NUL  , NUL    , NUL  , NUL   ,
               NUL   , B_PAO, NUL    , NUL  , NUL    , NUL  , NUL    , B_PAO, NUL   ,
               B_BING, NUL  , B_BING , NUL  , B_BING , NUL  , B_BING , NUL  , B_BING,
               NUL   , NUL  , NUL    , NUL  , NUL    , NUL  , NUL    , NUL  , NUL   ,
               NUL   , NUL  , NUL    , NUL  , NUL    , NUL  , NUL    , NUL  , NUL   ,
               R_BING, NUL  , R_BING , NUL  , R_BING , NUL  , R_BING , NUL  , R_BING,
               NUL   , R_PAO, NUL    , NUL  , NUL    , NUL  , NUL    , R_PAO, NUL   ,
               NUL   , NUL  , NUL    , NUL  , NUL    , NUL  , NUL    , NUL  , NUL   ,
               R_JU  , R_MA , R_XIANG, R_SHI, R_JIANG, R_SHI, R_XIANG, R_MA , R_JU  };
    m_cur_player_id = 1;
    m_left_action_num = 200;
}

std::string ChessState::to_compact_string() const {
    std::ostringstream oss;
    for (int i = 0; i < BOARD_HEIGHT; ++i) {
        for (int j = 0; j < BOARD_WIDTH; ++j) {
            oss << m_board[i][j];
        }
    }
    return oss.str();
}

std::string ChessState::to_string() const {
    std::ostringstream oss;
    for (int i = 0; i < BOARD_HEIGHT; ++i) {
        for (int j = 0; j < BOARD_WIDTH; ++j) {
            oss << m_board[i][j];
            if (j != BOARD_WIDTH-1) oss << "  ";
        }
        if (i != BOARD_HEIGHT-1) oss << "\n\n";
    }
    return oss.str();
}

ChessState::Actions ChessState::get_legal_actions(int player_id) const {
    assert(m_cur_player_id==player_id);
    Actions legal_actions;
    int sign = player_id == 1 ? 1 : -1;
    for (int i = 0; i < BOARD_HEIGHT; ++i) {
        for (int j = 0; j < BOARD_WIDTH; ++j) {
            int p = m_board[i][j];
            if (p == R_JIANG*sign) append_legal_action_JIANG(legal_actions, i, j, sign);
            else if (p == R_SHI*sign) append_legal_action_SHI(legal_actions, i, j, sign);
            else if (p == R_XIANG*sign) append_legal_action_XIANG(legal_actions, i, j, sign);
            else if (p == R_BING*sign) append_legal_action_BING(legal_actions, i, j, sign);
            else if (p == R_PAO*sign) append_legal_action_PAO(legal_actions, i, j, sign);
            else if (p == R_MA*sign) append_legal_action_MA(legal_actions, i, j, sign);
            else if (p == R_JU*sign) append_legal_action_JU(legal_actions, i, j, sign);
        }
    }
    for (const auto &action : legal_actions) {
        if (m_cur_player_id == 1 && m_board[action[2]][action[3]] == B_JIANG ||
            m_cur_player_id == 2 && m_board[action[2]][action[3]] == R_JIANG) {
            return Actions{action};
        }
    }
    return legal_actions;
}

int ChessState::get_result() const {
    if (m_cur_player_id == 1) {
        bool player2_wins = true;
        for (const auto &row : m_board) {
            if (std::find(std::begin(row), std::end(row), int(R_JIANG)) != std::end(row)) {
                player2_wins = false;
                break;
            }
        }
        if (player2_wins) return 2;
    } else {
        bool player1_wins = true;
        for (const auto& row : m_board) {
            if (std::find(std::begin(row), std::end(row), int(B_JIANG)) != std::end(row)) {
                player1_wins = false;
                break;
            }
        }
        if (player1_wins) return 1;
    }
    return m_left_action_num == 0 ? 0 : -1;
}

void ChessState::do_action(int player_id, const Action& action) {
    assert(m_cur_player_id==player_id);
    assert(player_id==1 && m_board[action[0]][action[1]]>NUL ||
           player_id==2 && m_board[action[0]][action[1]]<NUL);
    assert(player_id==1 && m_board[action[2]][action[3]]<=NUL ||
           player_id==2 && m_board[action[2]][action[3]]>=NUL);
    m_board[action[2]][action[3]] = m_board[action[0]][action[1]];
    m_board[action[0]][action[1]] = NUL;
    --m_left_action_num;
    m_cur_player_id = get_next_player_id(player_id);
}

void ChessState::append_legal_action_JIANG(Actions& legal_actions, int i, int j, int sign) const {
    if ((m_cur_player_id == 1 && i-1 >= 7 || m_cur_player_id == 2 && i-1 >= 0) && m_board[i-1][j]*sign <= NUL) legal_actions.push_back({i, j, i-1, j});
    if ((m_cur_player_id == 1 && i+1 < BOARD_HEIGHT || m_cur_player_id == 2 && i+1 <= 2) && m_board[i+1][j]*sign <= NUL) legal_actions.push_back({i, j, i+1, j});
    if (j-1 >= 3 && m_board[i][j-1]*sign <= NUL) legal_actions.push_back({i, j, i, j-1});
    if (j+1 <= 5 && m_board[i][j+1]*sign <= NUL) legal_actions.push_back({i, j, i, j+1});
    if (m_cur_player_id == 1) {
        int i1 = 0;
        while (i1 <= 2 && m_board[i1][j] != B_JIANG) ++i1;
        if (i1 <= 2) {
            int i2 = i1+1;
            while (i2 != i && m_board[i2][j] == NUL) ++i2;
            if (i2 == i) legal_actions.push_back({i, j, i1, j});
        }
    } else {
        int i1 = BOARD_HEIGHT-1;
        while (i1 >= 7 && m_board[i1][j] != R_JIANG) --i1;
        if (i1 >= 7) {
            int i2 = i1-1;
            while (i2 != i && m_board[i2][j] == NUL) --i2;
            if (i2 == i) legal_actions.push_back({i, j, i1, j});
        }
    }
}

void ChessState::append_legal_action_SHI(Actions& legal_actions, int i, int j, int sign) const {
    if (m_cur_player_id == 1 && i-1 >= 7 || m_cur_player_id == 2 && i-1 >= 0) {
        if (j-1 >= 3 && m_board[i-1][j-1]*sign <= NUL) legal_actions.push_back({i, j, i-1, j-1});
        if (j+1 <= 5 && m_board[i-1][j+1]*sign <= NUL) legal_actions.push_back({i, j, i-1, j+1});
    }
    if (m_cur_player_id == 1 && i+1 < BOARD_HEIGHT || m_cur_player_id == 2 && i+1 <= 2) {
        if (j-1 >= 3 && m_board[i+1][j-1]*sign <= NUL) legal_actions.push_back({i, j, i+1, j-1});
        if (j+1 <= 5 && m_board[i+1][j+1]*sign <= NUL) legal_actions.push_back({i, j, i+1, j+1});
    }
}

void ChessState::append_legal_action_XIANG(Actions& legal_actions, int i, int j, int sign) const {
    if (m_cur_player_id == 1 && i-2 >= 5 || m_cur_player_id == 2 && i-2 >= 0) {
        if (j-2 >= 0 && m_board[i-1][j-1] == NUL && m_board[i-2][j-2]*sign <= NUL) legal_actions.push_back({i, j, i-2, j-2});
        if (j+2 < BOARD_WIDTH && m_board[i-1][j+1] == NUL && m_board[i-2][j+2]*sign <= NUL) legal_actions.push_back({i, j, i-2, j+2});
    }
    if (m_cur_player_id == 1 && i+2 < BOARD_HEIGHT || m_cur_player_id == 2 && i+2 <= 4) {
        if (j-2 >= 0 && m_board[i+1][j-1] == NUL && m_board[i+2][j-2]*sign <= NUL) legal_actions.push_back({i, j, i+2, j-2});
        if (j+2 < BOARD_WIDTH && m_board[i+1][j+1] == NUL && m_board[i+2][j+2]*sign <= NUL) legal_actions.push_back({i, j, i+2, j+2});
    }
}

void ChessState::append_legal_action_BING(Actions& legal_actions, int i, int j, int sign) const {
    if ((m_cur_player_id == 1 && i-1 >=0 || m_cur_player_id == 2 && i+1 < BOARD_HEIGHT) && m_board[i-sign][j]*sign <= NUL) legal_actions.push_back({i, j, i-sign, j});
    if (m_cur_player_id == 1 && i <= 4 || m_cur_player_id == 2 && i >= 5) {
        if (j-1 >= 0 && m_board[i][j-1]*sign <= NUL) legal_actions.push_back({i, j, i, j-1});
        if (j+1 < BOARD_WIDTH && m_board[i][j+1]*sign <= NUL) legal_actions.push_back({i, j, i, j+1});
    }
}

void ChessState::append_legal_action_PAO(Actions& legal_actions, int i, int j, int sign) const {
    int i1;
    // up
    i1 = i-1;
    while (i1 >= 0 && m_board[i1][j] == NUL) {
        legal_actions.push_back({i, j, i1, j});
        --i1;
    }
    --i1;
    while (i1 >= 0 && m_board[i1][j] == NUL) --i1;
    if (i1 >= 0 && m_board[i1][j]*sign <= NUL) legal_actions.push_back({i, j, i1, j});
    // down
    i1 = i+1;
    while (i1 < BOARD_HEIGHT && m_board[i1][j] == NUL) {
        legal_actions.push_back({i, j, i1, j});
        ++i1;
    }
    ++i1;
    while (i1 < BOARD_HEIGHT && m_board[i1][j] == NUL) ++i1;
    if (i1 < BOARD_HEIGHT && m_board[i1][j]*sign <= NUL) legal_actions.push_back({i, j, i1, j});
    int j1;
    // left
    j1 = j-1;
    while (j1 >= 0 && m_board[i][j1] == NUL) {
        legal_actions.push_back({i, j, i, j1});
        --j1;
    }
    --j1;
    while (j1 >= 0 && m_board[i][j1] == NUL) --j1;
    if (j1 >= 0 && m_board[i][j1]*sign <= NUL) legal_actions.push_back({i, j, i, j1});
    // right
    j1 = j+1;
    while (j1 < BOARD_WIDTH && m_board[i][j1] == NUL) {
        legal_actions.push_back({i, j, i, j1});
        ++j1;
    }
    ++j1;
    while (j1 < BOARD_WIDTH && m_board[i][j1] == NUL) ++j1;
    if (j1 < BOARD_WIDTH && m_board[i][j1]*sign <= NUL) legal_actions.push_back({i, j, i, j1});
}

void ChessState::append_legal_action_MA(Actions& legal_actions, int i, int j, int sign) const {
    if (i-2 >= 0 && m_board[i-1][j] == NUL) {
        if (j-1 >= 0 && m_board[i-2][j-1]*sign <= NUL) legal_actions.push_back({i, j, i-2, j-1});
        if (j+1 < BOARD_WIDTH && m_board[i-2][j+1]*sign <= NUL) legal_actions.push_back({i, j, i-2, j+1});
    }
    if (i+2 < BOARD_HEIGHT && m_board[i+1][j] == NUL) {
        if (j-1 >= 0 && m_board[i+2][j-1]*sign <= NUL) legal_actions.push_back({i, j, i+2, j-1});
        if (j+1 < BOARD_WIDTH && m_board[i+2][j+1]*sign <= NUL) legal_actions.push_back({i, j, i+2, j+1});
    }
    if (j-2 >= 0 && m_board[i][j-1] == NUL) {
        if (i-1 >= 0 && m_board[i-1][j-2]*sign <= NUL) legal_actions.push_back({i, j, i-1, j-2});
        if (i+1 < BOARD_HEIGHT && m_board[i+1][j-2]*sign <= NUL) legal_actions.push_back({i, j, i+1, j-2});
    }
    if (j+2 < BOARD_WIDTH && m_board[i][j+1] == NUL) {
        if (i-1 >= 0 && m_board[i-1][j+2]*sign <= NUL) legal_actions.push_back({i, j, i-1, j+2});
        if (i+1 < BOARD_HEIGHT && m_board[i+1][j+2]*sign <= NUL) legal_actions.push_back({i, j, i+1, j+2});
    }
}

void ChessState::append_legal_action_JU(Actions& legal_actions, int i, int j, int sign) const {
    int i1;
    // up
    i1 = i-1;
    while (i1 >= 0) {
        if (m_board[i1][j]*sign <= NUL) legal_actions.push_back({i, j, i1, j});
        if (m_board[i1][j]*sign != NUL) break;
        --i1;
    }
    // down
    i1 = i+1;
    while (i1 < BOARD_HEIGHT) {
        if (m_board[i1][j]*sign <= NUL) legal_actions.push_back({i, j, i1, j});
        if (m_board[i1][j]*sign != NUL) break;
        ++i1;
    }
    int j1;
    // left
    j1 = j-1;
    while (j1 >= 0) {
        if (m_board[i][j1]*sign <= NUL) legal_actions.push_back({i, j, i, j1});
        if (m_board[i][j1]*sign != NUL) break;
        --j1;
    }
    // right
    j1 = j+1;
    while (j1 < BOARD_WIDTH) {
        if (m_board[i][j1]*sign <= NUL) legal_actions.push_back({i, j, i, j1});
        if (m_board[i][j1]*sign != NUL) break;
        ++j1;
    }
}

