import itertools

def get_next_player_id(player_id):
    return 3 - player_id

def save_transcript(transcript_path, actions):
    with open(transcript_path, 'w') as f:
        for player_id, action in zip(itertools.cycle((1, 2)), actions):
            line = '{0} {1}\n'.format(player_id, ','.join(map(str, action)))
            f.write(line)

