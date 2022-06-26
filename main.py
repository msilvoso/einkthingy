import logging
import os
import time
import RPi.GPIO as GPIO
from waveshare_epd import epd2in7
from PIL import Image, ImageDraw, ImageFont

from epaper.internetrefresh import InternetRefresh
from epaper.timer import Timer

logging.basicConfig(level=logging.DEBUG)
GPIO.setmode(GPIO.BCM)

key1 = 5
key2 = 6
key3 = 13
key4 = 19

font = "/usr/local/share/fonts/Roboto-Light.ttf"
font18 = ImageFont.truetype(font, 18)
font24 = ImageFont.truetype(font, 24)
font35 = ImageFont.truetype(font, 35)

epd = epd2in7.EPD()

GPIO.setup(key1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key2, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key3, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(key4, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def display(text, switch):
    logging.debug(text)
    epd.init()
    # epd.Clear(0xFF)
    himage = Image.new('1', (epd.height, epd.width), epd.GRAY1)  # 255: clear the frame
    draw = ImageDraw.Draw(himage)
    draw.text((0, 0), text, font=font35, fill=epd.GRAY4)
    draw.text((epd.height - 30, 16), switch, font=font18, fill=epd.GRAY4)
    draw.line((epd.height, 0, epd.height - 16, 0), fill=epd.GRAY4, width=5)
    draw.line((epd.height, 0, epd.height, 16), fill=epd.GRAY4, width=5)
    draw.line((epd.height, 0, epd.height - 16, 16), fill=epd.GRAY4, width=5)
    im_rotate = himage.rotate(180)
    epd.display(epd.getbuffer(im_rotate))
    epd.sleep()


# timers and states
# avoid calling internet on or off twice
internet_button_timer = Timer(1)
# is the internet on status
internet_state = InternetRefresh()


def button1(channel):
    display("Only key4 works!", "")


def button2(channel):
    display("Only key4 works!", "")


def button3(channel):
    display("Only key4 works!", "")


def button4(channel):
    if not internet_button_timer.over():
        return
    # wait for 5 minutes before function can be called again
    internet_button_timer.start(300)
    if InternetRefresh.fritz_on():
        display("Switching off", "-")
        os.system("/usr/local/bin/shutdownfw")
        return
    display("Switching on", "-")
    os.system("/usr/local/bin/fritzon.php")


GPIO.add_event_detect(key1, GPIO.FALLING, callback=button1, bouncetime=200)
GPIO.add_event_detect(key2, GPIO.FALLING, callback=button2, bouncetime=200)
GPIO.add_event_detect(key3, GPIO.FALLING, callback=button3, bouncetime=200)
GPIO.add_event_detect(key4, GPIO.FALLING, callback=button4, bouncetime=200)


def infinite_loop():
    try:
        logging.info("Ready")
        while True:
            if internet_state.dirty:
                if internet_state.state:
                    display_text = "Internet is on"
                    button_legend = "off"
                    display(display_text, button_legend)
                else:
                    display_text = "Internet is off"
                    button_legend = "on"
                    display(display_text, button_legend)
            internet_state.refresh()
            time.sleep(1)

    except KeyboardInterrupt:
        logging.info("ctrl + c:")
        epd2in7.epdconfig.module_exit()
        GPIO.cleanup()
        logging.info("\nBye")


infinite_loop()
