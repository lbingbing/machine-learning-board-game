from board_game.players import player

class TranscriptPlayer(player.Player):
    type = player.TRANSCRIPT_PLAYER

    def __init__(self, player_id, transcript_path):
        super().__init__(player_id)

        self.actions = []
        with open(transcript_path) as f:
            for line in f:
                player_id, action = line.split()
                player_id = int(player_id)
                if player_id == self.player_id:
                    action = tuple(map(int, action.split(',')))
                    self.actions.append(action)
        self.action_index = 0

    def get_action(self, state):
        super().get_action(state)
        action = self.actions[self.action_index]
        self.action_index = (self.action_index + 1) % len(self.actions)
        assert(action in state.get_legal_actions(self.player_id))
        return action

