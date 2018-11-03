#include <iostream>
#include <cstdio>

#include "BlackWhiteState.h"
#include "Mcts.h"

void print(const BlackWhiteState& state) {
    std::cout << state.to_string() << std::endl;
}

int main(){
    std::array<int, 3> scores{};
    GomokuState state{9, 9, 5};
    auto print_lambda = [&scores]() { std::cout << "\rp1/p2/draw " << scores[1] << "/" << scores[2] << "/" << scores[0]; };
    print_lambda();
    for (int i = 0; i < 10; ++i) {
        state.reset();
        //print(state);
        int player_id = 1;
        while (1) {
            MctsTree<BlackWhiteState> mcts_tree{state, player_id, 10000};
            BlackWhiteState::Action action = mcts_tree.get_action(state, player_id);
            //BlackWhiteState::Action action = mcts_tree.get_action_smt(state, player_id);
            state.do_action(player_id, action);
            //std::cout << "player " << player_id << ": " << action << std::endl;
            //print(state);
            //std::cout << "pause";
            //getchar();
            if (state.is_end()) break;
            player_id = BlackWhiteState::get_next_player_id(player_id);
        }
        //std::cout << "player " << player_id << " wins " << std::endl;
        int result = state.get_result();
        ++scores[result];
        print_lambda();
    }
    std::cout << std::endl;
    return 0;
}
