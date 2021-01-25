"""
    CranPiTFT - An object embodying some useful functions for the Adafruit TFT display.
    For now, only supports the 1.3" display, st7789, 240x240.
    @author robcranfill@robcranfill.net

    For the drawing methods we pass through,
    @see https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html

    Note that NONE of the pass-thru drawing methods call 'updateImage()' - you must do that after done drawing.
    (I do this cuz it presumably is faster this way: do all your drawing, then call updateImage().)
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

        self.width  = 240 # for 1.3" display
        self.height = 240 # for 1.3" display
        self.rotation = rotation

        # for convenience, here
        width = self.width
        height = self.height
        rotation = self.rotation

        # Create the ST7789 display:
        self.disp = st7789.ST7789(
            board.SPI(), # Set up SPI bus using hardware SPI
            cs = digitalio.DigitalInOut(board.CE0),
            dc = digitalio.DigitalInOut(board.D25),
            rst = None,
            baudrate = 64000000,
            width = width,
            height = height,
            x_offset = 0, # for 1.3" display
            y_offset = 80 # for 1.3" display
        )
        disp = self.disp

        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        # height = disp.width  # we swap height/width to rotate it to landscape!
        # width = disp.height

        self.image = Image.new("RGB", (width, height))
        image = self.image

        # rotation = 180

        # Get drawing object to draw on image.
        self.draw = ImageDraw.Draw(image)

        # Create access to backlight - and turn it on
        backlight = digitalio.DigitalInOut(board.D22)
        self.backlight = backlight
        backlight.switch_to_output()
        backlight.value = True

        self.clearToBlack()

        disp.image(image, rotation)



    def line(self, xy, fill=None, width=0, joint=None):
        self.draw.line(xy, fill, width, joint)

    def rectangle(self, xy, fill=None, outline=None, width=1):
        self.draw.rectangle(xy, fill, outline, width)

    def ellipse(self, xy, fill=None, outline=None, width=1):
        self.draw.ellipse(xy, fill, outline, width)

    def pieslice(self, xy, start, end, fill=None, outline=None, width=1):
        self.draw.pieslice(xy, start, end, fill, outline, width)

    def point(self, xy, fill=None):
        self.draw.point(self, xy, fill)

    def polygon(self, xy, fill=None, outline=None):
        self.draw.polygon(self, xy, fill, outline)

    def regular_polygon(self, bounding_circle, n_sides, rotation=0, fill=None, outline=None):
        self.draw.regular_polygon(self, bounding_circle, n_sides, rotation, fill, outline)

    def rectangle(self, xy, fill=None, outline=None, width=1):
        self.draw.rectangle(self, xy, fill, outline, width)

    def text(self, xy, text, fill=None, font=None, anchor=None, spacing=4, align='left', direction=None,
                features=None, language=None, stroke_width=0, stroke_fill=None, embedded_color=False):
        self.draw.text(self, xy, text, fill, font, anchor, spacing, align, direction,
                    features, language, stroke_width, stroke_fill, embedded_color)

    """
        Call this when you have drawn all your stuff.
    """
    def updateImage(self):
        self.disp.image(self.image, self.rotation)


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
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        self.disp.image(self.image, self.rotation)

        # Draw a black filled box to clear the image.
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=0)

        # Display image.
        self.disp.image(self.image, self.rotation)

    """
    We could do more methods like this... useful? probably not.
    """
    def makeAnX(self):
        w = self.width
        h = self.height
        self.draw.line([(0, 0), (w, h)], fill=(255, 0, 0), width=4)
        self.draw.line([(0, h), (w, 0)], fill=(255, 0, 0), width=4)
        self.updateImage()
