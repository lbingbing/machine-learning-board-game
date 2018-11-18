from board_game.players import player

class HumanPlayer(player.Player):
    type = player.HUMAN_PLAYER

    def get_action(self, state):
        super().get_action(state)
        # input action in format 'y,x', 'y0,x0,y1,x1'
        while True:
            action_str = input()
            try:
                action = action_str.split(',')
                action = tuple(map(int, action))
                if action not in state.get_legal_actions(self.player_id):
                    raise ValueError
                break
            except ValueError:
                print("illegal action '{0}'".format(action_str))
        return action

