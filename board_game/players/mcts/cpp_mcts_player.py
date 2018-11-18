import subprocess

from board_game.players import player

class CppMctsPlayer(player.Player):
    type = player.CPP_MCTS_PLAYER

    def __init__(self, player_id, sim_num):
        super().__init__(player_id)

        self.sim_num = sim_num

    def get_cmd_str(self, state):
        pass

    def get_action(self, state):
        super().get_action(state)
        res = subprocess.run(self.get_cmd_strs(state) + [str(self.sim_num)], stdout = subprocess.PIPE, check = True, encoding = 'utf-8')
        action = tuple(map(int, res.stdout.strip()[1:-1].split(', ')))
        return action

