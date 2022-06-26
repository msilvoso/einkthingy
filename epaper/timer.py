import time


class Timer:
    stop = 0.0
    wait = 0.0

    def __init__(self, wait):
        self.start(wait)

    def start(self, wait):
        self.stop = time.time()
        self.wait = wait

    def over(self):
        now = time.time()
        return self.stop + self.wait < now

    def over_and_restart(self):
        now = time.time()
        over = self.stop + self.wait < now
        if over:
            self.start(self.wait)
        return over
