import logging
import os
import time
import RPi.GPIO as GPIO
from waveshare_epd import epd2in7

from epaper.internetrefresh import InternetRefresh
from epaper.trashrefresh import TrashRefresh
from epaper.shutdowntimerrefresh import ShutdownTimerRefresh
from epaper.stimerefresh import STimeRefresh
from epaper.timer import Timer
from epaper.state import EpaperState
from epaper.display import Display

logging.basicConfig(level=logging.DEBUG)
GPIO.setmode(GPIO.BCM)

key1 = 5
key2 = 6
key3 = 13
key4 = 19

GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

display = Display()
# timers and states
# avoid calling internet on or off twice
internet_button_timer = Timer(1)
# refresh every hour
hourly_timer = Timer(3600)
# is the internet on status
state = EpaperState()
state.states["internet_state"] = InternetRefresh()
# the trash
state.states["trash_state"] = TrashRefresh("/usr/local/share/VDL.ics")
# the shutdown timer
state.states["shutdown_timer_enabled"] = ShutdownTimerRefresh()
# shutdown time
state.states["shutdown_time"] = STimeRefresh()
# loop sleep time
loop_sleep_time = 1

def button1(channel):
    state.refresh(True)
    state.make_dirty()


def button2(channel):
    state.refresh(True)
    state.make_dirty()
    if state.states["shutdown_timer_enabled"].state:
        os.system("/usr/bin/systemctl disable shutdownfw.timer --now")
        return
    os.system("/usr/bin/systemctl enable shutdownfw.timer --now")


def button3(channel):
    display.display(state, "Only key4 works")


def button4(channel):
    if not internet_button_timer.over():
        return
    # wait for 5 minutes before function can be called again
    internet_button_timer.start(300)
    if InternetRefresh.fritz_on():
        display.display(state, "Switching off")
        os.system("/usr/local/bin/shutdownfw")
        return
    display.display(state, "Switching on")
    os.system("/usr/local/bin/fritzon.php")


GPIO.add_event_detect(key1, GPIO.FALLING, callback=button1, bouncetime=200)
GPIO.add_event_detect(key2, GPIO.FALLING, callback=button2, bouncetime=200)
GPIO.add_event_detect(key3, GPIO.FALLING, callback=button3, bouncetime=200)
GPIO.add_event_detect(key4, GPIO.FALLING, callback=button4, bouncetime=200)


def infinite_loop():
    try:
        logging.info("Ready")
        while True:
            global loop_sleep_time
            if state.dirty() or hourly_timer.over_and_restart():
                display.display(state)
            state.refresh()
            time.sleep(loop_sleep_time)
            loop_sleep_time = 1

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd2in7.epdconfig.module_exit()
        GPIO.cleanup()
        logging.info("\nBye")


infinite_loop()
