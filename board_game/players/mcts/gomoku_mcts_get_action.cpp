#include <iostream>
#include <cassert>

#include "gomoku_state.h"
#include "mcts.h"

int main(int argc, char* argv[]) {
    assert(argc==7);
    int board_height = std::stoi(argv[1]);
    int board_width = std::stoi(argv[2]);
    std::string state_compact_str{argv[3]};
    int player_id = std::stoi(argv[4]);
    int target = std::stoi(argv[5]);
    int sim_num = std::stoi(argv[6]);
    GomokuState state{board_height, board_width, target, state_compact_str, player_id};
    MctsTree<GomokuState> mcts_tree{state, player_id, sim_num};
    //GomokuState::Action action = mcts_tree.get_action(state, player_id);
    GomokuState::Action action = mcts_tree.get_action_smt(state, player_id);
    std::cout << action << std::endl;

    return 0;
}

