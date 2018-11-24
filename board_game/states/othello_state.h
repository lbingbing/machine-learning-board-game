#ifndef __OTHELLO_STATE_H__
#define __OTHELLO_STATE_H__

#include "blackwhite_state.h"

class OthelloState : public BlackWhiteState {
public:
    OthelloState(int board_height, int board_width);
    OthelloState(int board_height, int board_width, const std::string& state_compact_str, int player_id) : BlackWhiteState(board_height, board_width, state_compact_str, player_id) {}

    void         reset();
    Actions      get_legal_actions(int player_id) const;
    virtual int  get_result() const override;
    void         do_action(int player_id, const Action& action);

private:
    using TargetPos = std::array<int, 2>;

    void       reset_self();
    TargetPos  get_target_pos(int i, int j, int idir, int jdir, int player_id, int opponent_player_id) const;
    void       change_color(int i, int j, int idir, int jdir, int player_id, int opponent_player_id);
};

#endif

