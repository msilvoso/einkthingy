import logging
import os

from epaper.timer import Timer


class InternetRefresh:
    timer = Timer(240)
    state = False
    previous_state = False
    dirty = True

    def __init__(self):
        self.refresh(force=True)
        self.dirty = True

    def refresh(self, force=False):
        self.dirty = False
        if not self.timer.over_and_restart() and not force:
            return
        self.state = InternetRefresh.fritz_on()
        if self.state != self.previous_state:
            self.previous_state = self.state
            self.dirty = True

    @staticmethod
    def fritz_on():
        is_on = os.system("/usr/local/bin/fritzstate.php")
        logging.debug("Is the fritzbox on? " + str(is_on >> 8 == 10))
        return is_on >> 8 == 10
