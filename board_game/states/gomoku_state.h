#ifndef __GOMOKU_STATE_H__
#define __GOMOKU_STATE_H__

#include <string>

#include "blackwhite_state.h"

class GomokuState : public BlackWhiteState {
public:
    GomokuState(int board_height, int board_width, int target) : BlackWhiteState(board_height, board_width), m_target(target) {};
    GomokuState(int board_height, int board_width, int target, const std::string& state_compact_str, int player_id) : BlackWhiteState(board_height, board_width, state_compact_str, player_id), m_target(target) {}

    virtual int get_result() const override;

private:
    int m_target;
};

#endif

