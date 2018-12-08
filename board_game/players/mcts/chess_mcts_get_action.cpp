#include <iostream>
#include <cassert>

#include "chess_state.h"
#include "mcts.h"

int main(int argc, char* argv[]) {
    assert(argc==7);
    std::string state_compact_str{argv[1]};
    std::string board_history_compact_str{argv[2]};
    int player_id = std::stoi(argv[3]);
    int left_action_num = std::stoi(argv[4]);
    int left_no_kill_action_num = std::stoi(argv[5]);
    int sim_num = std::stoi(argv[6]);
    ChessState state{state_compact_str, board_history_compact_str, player_id, left_action_num, left_no_kill_action_num};
    MctsTree<ChessState> mcts_tree{state, player_id, sim_num};
    //ChessState::Action action = mcts_tree.get_action(state, player_id);
    ChessState::Action action = mcts_tree.get_action_smt(state, player_id);
    std::cout << action << std::endl;

    return 0;
}

