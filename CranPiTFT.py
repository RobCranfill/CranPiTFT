"""
    CranPiTFT - A library of useful functions for the Adafruit TFT display.
    Only supports the 1.3" display, st7789
    @author robcranfill@robcranfill.net


    TODO:
"""
# -*- coding: utf-8 -*-

import time
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565

class CranPiTFT:
    def __init__(self, rotation=90): # 90 default for 1.3" display

        self.width_  = 240 # for 1.3" display
        self.height_ = 240 # for 1.3" display
        self.rotation_ = rotation

        width = self.width_
        height = self.height_
        rotation = self.rotation_

        # Create the ST7789 display:
        self.disp_ = st7789.ST7789(
            board.SPI(), # Set up SPI bus using hardware SPI
            cs = digitalio.DigitalInOut(board.CE0),
            dc = digitalio.DigitalInOut(board.D25),
            rst = None,
            baudrate = 64000000,
            width = width,
            height = height,
            x_offset=0, # for 1.3" display
            y_offset=80 # for 1.3" display
        )
        disp = self.disp_

        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        # height = disp.width  # we swap height/width to rotate it to landscape!
        # width = disp.height

        self.image_ = Image.new("RGB", (width, height))
        image = self.image_

        # rotation = 180

        # Get drawing object to draw on image.
        self.draw_ = ImageDraw.Draw(image)
        # draw = self.draw_

        # Create access to backlight - and turn it on
        backlight = digitalio.DigitalInOut(board.D22)
        self.backlight_ = backlight
        backlight.switch_to_output()
        backlight.value = True

        self.clearToBlack()

        disp.image(image, rotation)

    """
        Note that this does NOT call updateImage - you must do that after done drawing.
    """
    def line(self, xy, fill=None, width=0, joint=None):
        self.draw_.line(xy, fill, width, joint)

    """
        Note that this does NOT call updateImage - you must do that after done drawing.
    """
    def rectangle(self, xy, fill=None, outline=None, width=1):
        self.draw_.rectangle(xy, fill, outline, width)


    def ellipse(self, xy, fill=None, outline=None, width=1):
        self.draw_.ellipse(xy, fill=None, outline=None, width=1)


    def pieslice(self, xy, start, end, fill=None, outline=None, width=1):
        self.draw_.pieslice(xy, start, end, fill=None, outline=None, width=1)
        pass

    def point(self, xy, fill=None):
        pass

    def polygon(self, xy, fill=None, outline=None):
        pass

    def regular_polygon(self, bounding_circle, n_sides, rotation=0, fill=None, outline=None):
        pass

    def rectangle(self, xy, fill=None, outline=None, width=1):
        pass

    def text(self, xy, text, fill=None, font=None, anchor=None, spacing=4, align='left', direction=None,
                features=None, language=None, stroke_width=0, stroke_fill=None, embedded_color=False):
        pass


    def updateImage(self):
        self.disp_.image(self.image_, self.rotation_)


    def setBacklight(self, backlightState):
        """
        Set the backlight as indicated.
        """
        self.backlight.value = backlightState


    def clearToBlack(self):
        """
        Clear the LCD display to all black. Does NOT turn off the backlight.
        """

        # Draw a black filled box to clear the image.
        self.draw_.rectangle((0, 0, self.width_, self.height_), outline=0, fill=(0, 0, 0))
        self.disp_.image(self.image_, self.rotation_)

        # Draw a black filled box to clear the image.
        self.draw_.rectangle((0, 0, self.width_, self.height_), outline=0, fill=0)

        # Display image.
        self.disp_.image(self.image_, self.rotation_)

    """
    We could do more methods like this... useful? probably not.
    """
    def makeAnX(self):
        w = self.width_
        h = self.height_
        self.draw_.line([(0, 0), (w, h)], fill=(255, 0, 0), width=4)
        self.draw_.line([(0, h), (w, 0)], fill=(255, 0, 0), width=4)
        self.updateImage()
