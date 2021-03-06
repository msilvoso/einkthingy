import logging
from waveshare_epd import epd2in7
from PIL import Image, ImageDraw, ImageFont


# Display resolution
# HEIGHT       = 176
# WIDTH        = 264


class Display:
    def __init__(self):
        font = "/usr/local/share/fonts/Roboto-Light.ttf"
        self.font18 = ImageFont.truetype(font, 18)
        self.font24 = ImageFont.truetype(font, 24)
        self.font35 = ImageFont.truetype(font, 35)
        self.epd = epd2in7.EPD()

    def display(self, state, message=""):
        self.epd.init()
        # self.epd.Clear(0xFF)
        himage = Image.new('1', (self.epd.height, self.epd.width), self.epd.GRAY1)  # 255: clear the frame
        # temperature data
        graph = Image.open(r'/var/lib/ems-esp/graph.png')
        himage.paste(graph.crop((0, 0, graph.width - 20, graph.height)), (20, 20))
        draw = ImageDraw.Draw(himage)
        vert = 30
        temperature_labels = ["wt:", "ft:", "ot:"]
        label_index = 0
        with open('/var/lib/ems-esp/lastvalues') as f:
            for line in f:
                draw.text((0, vert), temperature_labels[label_index], font=self.font18, fill=self.epd.GRAY4)
                vert += 20
                draw.text((0, vert), line, font=self.font18, fill=self.epd.GRAY4)
                vert += 20
                label_index += 1

        # message and Internet
        if message != "":
            draw.text((0, 0), message, font=self.font24, fill=self.epd.GRAY4)
            logging.debug("Display: {0}".format(message))
        else:
            if state.states["internet_state"].state:
                draw.text((0, 0), "Internet is on", font=self.font24, fill=self.epd.GRAY4)
                logging.debug("Display: Internet is on")
                draw.text((self.epd.height - 40, 5), "off", font=self.font18, fill=self.epd.GRAY4)
            else:
                draw.text((0, 0), "Internet is off", font=self.font24, fill=self.epd.GRAY4)
                logging.debug("Display: Internet is off")
                draw.text((self.epd.height - 40, 5), "on", font=self.font18, fill=self.epd.GRAY4)
            draw.line((self.epd.height, 0, self.epd.height - 16, 0), fill=self.epd.GRAY4, width=5)
            draw.line((self.epd.height, 0, self.epd.height, 16), fill=self.epd.GRAY4, width=5)
            draw.line((self.epd.height, 0, self.epd.height - 16, 16), fill=self.epd.GRAY4, width=5)
        # Trash info
        draw.text((60, 132), "d+1", font=self.font18, fill=self.epd.GRAY4)
        draw.text((150, 132), "d+2", font=self.font18, fill=self.epd.GRAY4)
        draw.text((0, 157), "Trash:", font=self.font18, fill=self.epd.GRAY4)
        draw.text((60, 151), state.states["trash_state"].state[0], font=self.font24, fill=self.epd.GRAY4)
        draw.text((150, 151), state.states["trash_state"].state[1], font=self.font24, fill=self.epd.GRAY4)
        # shutdown timer button
        if state.states["shutdown_timer_enabled"].state:
            draw.text((220, 81), "leave", font=self.font18, fill=self.epd.GRAY4)
            draw.text((230, 100), "on", font=self.font18, fill=self.epd.GRAY4)
        else:
            draw.text((220, 81), "auto", font=self.font18, fill=self.epd.GRAY4)
            draw.text((230, 100), "off", font=self.font18, fill=self.epd.GRAY4)
        # shutdown time
        draw.text((220, 35), state.states["shutdown_time"].state, font=self.font18, fill=self.epd.GRAY4)

        # Refresh
        draw.text((200, 132), "refresh", font=self.font18, fill=self.epd.GRAY4)
        draw.line((self.epd.height, self.epd.width - 12, self.epd.height - 20, self.epd.width - 12),
                  fill=self.epd.GRAY4, width=5)
        draw.line((self.epd.height - 20, self.epd.width - 12, self.epd.height - 20, self.epd.width - 24),
                  fill=self.epd.GRAY4, width=5)
        draw.line((self.epd.height, self.epd.width - 12, self.epd.height - 12, self.epd.width - 24),
                  fill=self.epd.GRAY4, width=5)
        draw.line((self.epd.height, self.epd.width - 12, self.epd.height - 12, self.epd.width), fill=self.epd.GRAY4,
                  width=5)

        im_rotate = himage.rotate(180)
        self.epd.display(self.epd.getbuffer(im_rotate))
        self.epd.sleep()
