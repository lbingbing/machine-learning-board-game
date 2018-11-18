import random

from board_game.players import player

class RandomPlayer(player.Player):
    type = player.RANDOM_PLAYER

    def get_action(self, state):
        super().get_action(state)
        return random.choice(state.get_legal_actions(self.player_id))

