import logging
import os


class ShutdownTimerRefresh:
    state = False
    dirty = True

    def __init__(self):
        self.refresh(force=True)
        self.dirty = True

    def refresh(self, force=False):
        self.dirty = False
        if not force:
            return
        self.state = ShutdownTimerRefresh.shutdown_timer_enabled()

    @staticmethod
    def shutdown_timer_enabled():
        is_enabled = os.system("/usr/bin/systemctl is-enabled shutdownfw.timer")
        is_enabled = is_enabled >> 8
        logging.debug("Is the shutdown timer started? " + str(is_enabled == 0))
        return is_enabled == 0
