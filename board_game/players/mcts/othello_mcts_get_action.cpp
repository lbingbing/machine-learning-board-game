#include <iostream>
#include <cassert>

#include "othello_state.h"
#include "mcts.h"

int main(int argc, char* argv[]) {
    assert(argc==6);
    int board_height = std::stoi(argv[1]);
    int board_width = std::stoi(argv[2]);
    std::string state_compact_str{argv[3]};
    int player_id = std::stoi(argv[4]);
    int sim_num = std::stoi(argv[5]);
    OthelloState state{board_height, board_width, state_compact_str, player_id};
    MctsTree<OthelloState> mcts_tree{state, player_id, sim_num};
    //OthelloState::Action action = mcts_tree.get_action(state, player_id);
    OthelloState::Action action = mcts_tree.get_action_smt(state, player_id);
    std::cout << action << std::endl;

    return 0;
}

