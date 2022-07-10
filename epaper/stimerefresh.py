import logging
import re


class STimeRefresh:
    state = "01:00"
    dirty = True
    previous_state = "01:00"

    def __init__(self):
        self.refresh(force=True)
        self.dirty = True

    def refresh(self, force=False):
        self.dirty = False
        if not force:
            return
        self.state = STimeRefresh.shutdown_time()
        if self.state != self.previous_state:
            self.previous_state = self.state
            self.dirty = True

    @staticmethod
    def shutdown_time():
        f = open("/etc/systemd/system/shutdownfw.timer", "r")
        contents = f.read()
        f.close()
        shutdown_time = re.search(pattern=r'\d{2}:\d{2}', string=contents)
        logging.debug("Shutdown time: {time}".format(time=shutdown_time[0]))
        return shutdown_time[0]
