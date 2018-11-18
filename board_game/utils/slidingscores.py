class SlidingScores:
    def __init__(self, max_size):
        self.max_size = max_size
        self.window = []
        self.wr_ptr = 0

        self.scores = [0] * 3

    def update(self, result):
        if len(self.window) == self.max_size:
            self.scores[self.window[self.wr_ptr]] -= 1
            self.window[self.wr_ptr] = result
            self.wr_ptr = (self.wr_ptr+1) % self.max_size
        else:
            self.window.append(result)
        self.scores[result] += 1

