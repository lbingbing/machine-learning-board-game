#ifndef __State_H__
#define __State_H__

#include <array>
#include <vector>
#include <string>
#include <iostream>

class ChessState {
public:
    static constexpr int BOARD_WIDTH  = 9;
    static constexpr int BOARD_HEIGHT = 10;

    static constexpr int MAX_ACTION_NUM = 200;
    static constexpr int MAX_NO_KILL_ACTION_NUM = 50;
                     
    static constexpr int NUL     = 0;
    static constexpr int R_JIANG = 1;
    static constexpr int R_SHI   = 2;
    static constexpr int R_XIANG = 3;
    static constexpr int R_BING  = 4;
    static constexpr int R_PAO   = 5;
    static constexpr int R_MA    = 6;
    static constexpr int R_JU    = 7;
    static constexpr int B_JIANG = -1;
    static constexpr int B_SHI   = -2;
    static constexpr int B_XIANG = -3;
    static constexpr int B_BING  = -4;
    static constexpr int B_PAO   = -5;
    static constexpr int B_MA    = -6;
    static constexpr int B_JU    = -7;

    using Board = std::array<std::array<int, BOARD_WIDTH>, BOARD_HEIGHT>;
    using Action = std::array<int, 4>;
    using Actions = std::vector<Action>;

    ChessState() { reset(); }
    ChessState(const std::string& state_compact_str, const std::string& board_history_compact_str, int player_id, int left_action_num, int left_no_kill_action_num);

    void         reset();
    std::string  to_compact_string() const;
    std::string  to_string() const;
    Actions      get_legal_actions(int player_id) const;
    bool         is_end() const { return get_result() >= 0; }
    int          get_result() const;
    void         do_action(int player_id, const Action& action);

private:
    void append_legal_action_JIANG(Actions& legal_actions, int i, int j, int sign) const;
    void append_legal_action_SHI(Actions& legal_actions, int i, int j, int sign) const;
    void append_legal_action_XIANG(Actions& legal_actions, int i, int j, int sign) const;
    void append_legal_action_BING(Actions& legal_actions, int i, int j, int sign) const;
    void append_legal_action_PAO(Actions& legal_actions, int i, int j, int sign) const;
    void append_legal_action_MA(Actions& legal_actions, int i, int j, int sign) const;
    void append_legal_action_JU(Actions& legal_actions, int i, int j, int sign) const;

    Board               m_board;
    std::vector<Board>  m_board_history;
    int                 m_cur_player_id;
    int                 m_left_action_num;
    int                 m_left_no_kill_action_num;
};

inline std::ostream& operator<<(std::ostream& os, const ChessState::Action& action) {
    return os << "(" << action[0] << ", " << action[1] << ", " << action[2] << ", " << action[3] << ")";
}

#endif

