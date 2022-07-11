from datetime import datetime
from datetime import timedelta
import os

from epaper.timer import Timer
from epaper.stimerefresh import STimeRefresh
from epaper.shutdowntimerrefresh import ShutdownTimerRefresh

class STimeChange:
    def __init__(self):
        self.timer = Timer(0)
        self.dirty = False
        self.shutdown_time = STimeRefresh.shutdown_time()

    def add_10_min(self):
        if not self.dirty:
            self.dirty = True
            self.timer.start(10)
        shutdown_time = datetime.strptime(self.shutdown_time, "%H:%M")
        plus_10_min = timedelta(minutes=10)
        time_calc = shutdown_time + plus_10_min
        self.shutdown_time = time_calc.strftime("%H:%M")
        if "03:10" <= self.shutdown_time <= "12:00":
            self.shutdown_time = "23:00"

    def reload_shutdown_time(self, s_time_refresh):
        if self.dirty and self.timer.over():
            self.dirty = False
            STimeRefresh.set_shutdown_time(self.shutdown_time)
            s_time_refresh.refresh(force=True)
            os.system("/usr/bin/systemctl stop shutdownfw.timer")
            os.system("/usr/bin/systemctl daemon-reload")
            if ShutdownTimerRefresh.shutdown_timer_enabled():
                os.system("/usr/bin/systemctl start shutdownfw.timer")
