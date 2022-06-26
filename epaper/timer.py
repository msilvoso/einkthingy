import logging
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
        o = self.stop + self.wait < now
        if o:
            logging.debug("Timer with with time {0} : over with result {1}".format(self.wait, o))
        return o

    def over_and_restart(self):
        o = self.over()
        if o:
            self.start(self.wait)
        return o
