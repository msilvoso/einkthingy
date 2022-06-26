import datetime
import icalendar
from epaper.timer import Timer


class TrashRefresh:
    timer = Timer(12000)
    state = ["-", "-"]
    previous_state = ["-", "-"]
    dirty = True
    file = ""

    def __init__(self, file):
        self.file = file
        self.refresh(force=True)
        self.dirty = True

    def refresh(self, force=False):
        self.dirty = False
        if not self.timer.over_and_restart() and not force:
            return
        self.state = TrashRefresh.parse_ical(self.file)
        if self.state != self.previous_state:
            self.previous_state = self.state
            self.dirty = True

    @staticmethod
    def parse_ical(file):
        icalfile = open(file, 'rb')
        gcal = icalendar.Calendar.from_ical(icalfile.read())
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        the_day_after = tomorrow + datetime.timedelta(days=1)
        tomorrow_trash = []
        after_trash = []
        for component in gcal.walk():
            if component.name == "VEVENT":
                summary = component.get('summary')
                event = component.get('dtstart').dt.strftime("%Y-%m-%d")
                if event == tomorrow.strftime("%Y-%m-%d"):
                    if "residual" in summary.lower():
                        tomorrow_trash.append("black")
                    elif "food" in summary.lower():
                        tomorrow_trash.append("brown")
                    elif "valorlux" in summary.lower():
                        tomorrow_trash.append("blue")
                if event == the_day_after.strftime("%Y-%m-%d"):
                    if "residual" in summary.lower():
                        after_trash.append("black")
                    elif "food" in summary.lower():
                        after_trash.append("brown")
                    elif "valorlux" in summary.lower():
                        after_trash.append("blue")
        icalfile.close()
        t = ",".join(tomorrow_trash)
        if t == "":
            t = "-"
        a = ",".join(after_trash)
        if a == "":
            a = "-"
        return [t, a]
