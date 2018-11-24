from .cpp_mcts_player import CppMctsPlayer

class OthelloCppMctsPlayer(CppMctsPlayer):
    def get_cmd_strs(self, state):
        return ['board_game/players/mcts/release/othello_mcts_get_action.exe', str(state.board_shape[0]), str(state.board_shape[1]), state.compact_str(), str(state.get_cur_player_id())]

