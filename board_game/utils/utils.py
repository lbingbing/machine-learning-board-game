import numpy as np

def get_next_player_id(player_id):
    return 3 - player_id

def get_entropy(Ps_m):
    return np.sum(-np.log(Ps_m + 1e-20) * Ps_m) / np.log(Ps_m.shape[0])

