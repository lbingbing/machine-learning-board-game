from .cpp_mcts_player import CppMctsPlayer

class ChessCppMctsPlayer(CppMctsPlayer):
    def get_cmd_strs(self, state):
        return ['board_game/players/mcts/release/chess_mcts_get_action.exe', state.compact_str(), str(state.get_cur_player_id()), str(state.left_action_num)]

