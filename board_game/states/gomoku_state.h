#ifndef __GOMOKU_STATE_H__
#define __GOMOKU_STATE_H__

#include "blackwhite_state.h"

class GomokuState : public BlackWhiteState {
public:
    GomokuState(int board_height, int board_width, int target) : BlackWhiteState(board_height, board_width), m_target(target) {}
    GomokuState(int board_height, int board_width, int target, const std::string& state_compact_str, int player_id);

    void            reset();
    const Actions&  get_legal_actions(int player_id) const;
    virtual int     get_result() const override;
    void            do_action(int player_id, const Action& action);

private:
    int      m_target;
    Actions  m_legal_actions;
};

#endif

