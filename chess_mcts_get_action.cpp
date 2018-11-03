#include <iostream>
#include <cassert>

#include "ChessState.h"
#include "Mcts.h"

int main(int argc, char* argv[]) {
    assert(argc==5);
    std::string state_compact_str{argv[1]};
    int player_id = std::stoi(argv[2]);
    int left_action_num = std::stoi(argv[3]);
    int sim_num = std::stoi(argv[4]);
    ChessState state{state_compact_str, player_id, left_action_num};
    MctsTree<ChessState> mcts_tree{state, player_id, sim_num};
    //ChessState::Action action = mcts_tree.get_action(state, player_id);
    ChessState::Action action = mcts_tree.get_action_smt(state, player_id);
    std::cout << action << std::endl;

    return 0;
}
