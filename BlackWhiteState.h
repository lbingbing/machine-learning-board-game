#ifndef __BLACK_WHITE_STATE_H__
#define __BLACK_WHITE_STATE_H__

#include <array>
#include <vector>
#include <string>
#include <cassert>

class BlackWhiteState {
public:
    using Board = std::vector<std::vector<int>>;
    using Action = std::array<int, 2>;
    using Actions = std::vector<Action>;

    inline static int get_next_player_id(int player_id) { return 3 - player_id; }

    BlackWhiteState(int board_height, int board_width) : m_board_height(board_height), m_board_width(board_width), m_board(board_height, std::vector<int>(board_width)), m_legal_actions{} { reset(); }
    BlackWhiteState(int board_height, int board_width, const std::string& state_compact_str, int player_id);
    virtual BlackWhiteState* clone() const = 0;

    void           reset();
    std::string    to_compact_string() const;
    std::string    to_string() const;
    const Actions& get_legal_actions(int player_id) const { assert(m_last_player_id!=player_id); return m_legal_actions; }
    bool           is_end() const { return get_result() >= 0; }
    virtual int    get_result() const = 0;
    void           do_action(int player_id, const Action& action);

protected:
    int     m_board_height;
    int     m_board_width;
    Board   m_board;
    int     m_last_player_id;
    Action  m_last_action;
    int     m_piece_num;
    Actions m_legal_actions;
};

class GomokuState : public BlackWhiteState {
public:
    GomokuState(int board_height, int board_width, int target) : BlackWhiteState(board_height, board_width), m_target(target) {};
    GomokuState(int board_height, int board_width, int target, const std::string& state_compact_str, int player_id) : BlackWhiteState(board_height, board_width, state_compact_str, player_id), m_target(target) {}
    virtual GomokuState* clone () const override { return new GomokuState(*this); }

    virtual int get_result() const override;

private:
    int m_target;
};

inline std::ostream& operator<<(std::ostream& os, const BlackWhiteState::Action& action) {
    return os << "(" << action[0] << ", " << action[1] << ")";
}

#endif
