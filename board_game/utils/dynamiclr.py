class DynamicLR:
    def __init__(self, lr, min_lr, max_lr, avg_window_size, cmp_window_size):
        self.lr = lr
        self.min_lr = min_lr
        self.max_lr = max_lr
        self.avg_window_size = avg_window_size
        self.cmp_window_size = cmp_window_size
        self.losses = []
        self.avg_losses = []
        self.wait_cnt = cmp_window_size

    def update(self, loss):
        if self.wait_cnt > 0:
            self.wait_cnt -= 1

        self.losses.append(loss)
        if len(self.losses) > self.avg_window_size:
            del self.losses[0]

        avg_loss = sum(self.losses) / len(self.losses)
        self.avg_losses.append(avg_loss)
        if len(self.avg_losses) > self.cmp_window_size:
            del self.avg_losses[0]

        lr_changed = False
        if self.wait_cnt == 0:
            delta = self.avg_losses[-1] - self.avg_losses[0]
            if delta > 0:
                if self.lr > self.min_lr:
                    lr = self.lr / 1.5
                    lr_changed = True
            else:
                if self.lr < self.max_lr:
                    lr = self.lr * 1.2
                    lr_changed = True
        if lr_changed:
            self.lr = lr
            self.wait_cnt = self.cmp_window_size
        return lr_changed

import numpy as np

class DynamicLR1:
    def __init__(self, lr, min_lr, max_lr, window_size):
        self.lr = lr
        self.min_lr = min_lr
        self.max_lr = max_lr
        self.window_size = window_size
        self.losses = []
        self.max_trends_num = 3
        self.trends = []

    def update(self, loss):
        self.losses.append(loss)

        lr_changed = False
        if len(self.losses) == self.window_size:
            y_m = np.array(self.losses).reshape(-1, 1)
            x_m = np.ones((self.window_size, 2))
            x_m[:,1:2] = np.array(range(self.window_size)).reshape(-1, 1)
            theta_m = np.dot(np.dot(np.linalg.pinv(np.dot(x_m.T, x_m)), x_m.T), y_m)
            trend = -1 if theta_m[1] < 0 else 1
            self.trends.append(trend)
            if len(self.trends) > self.max_trends_num:
                del self.trends[0]

            if self.trends[-1] == 1:
                if self.lr > self.min_lr:
                    lr = self.lr / 1.5
                    lr_changed = True
            elif all(e == -1 for e in self.trends):
                if self.lr < self.max_lr:
                    lr = self.lr * 1.5
                    lr_changed = True
            self.losses = []

        if lr_changed:
            self.lr = lr
        return lr_changed

def test():
    import math
    import random
    import matplotlib.pyplot

    dlr = DynamicLR(lr = 1, min_lr = 0.0001, max_lr = 1, avg_window_size = 100, cmp_window_size = 10)
    #dlr = DynamicLR1(lr = 1, min_lr = 0.0001, max_lr = 1, window_size = 50)
    losses = [-i * 0.001 + 0.1 * math.sin(i*0.01) + 0.03 * math.sin(i*0.1) + 0.01 * math.sin(i) + 0.5 * random.random() for i in range(5000)]
    avg_losses = []
    lrs = []
    for e in losses:
        dlr.update(e)
        avg_losses.append(dlr.avg_losses[-1])
        lrs.append(dlr.lr)
    matplotlib.pyplot.subplot(2, 1, 1)
    matplotlib.pyplot.plot(losses)
    matplotlib.pyplot.plot(avg_losses)
    matplotlib.pyplot.subplot(2, 1, 2)
    matplotlib.pyplot.plot(lrs)
    matplotlib.pyplot.draw()
    matplotlib.pyplot.show()

if __name__ == '__main__':
    test()

