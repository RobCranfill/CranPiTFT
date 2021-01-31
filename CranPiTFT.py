#!/usr/bin/python
# -*- coding: utf-8 -*-
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

import time
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from adafruit_rgb_display.rgb import color565

class CranPiTFT:
    def __init__(self, rotation=90): # 90 default for 1.3" display

        self._width  = 240 # for 1.3" display
        self._height = 240 # for 1.3" display
        self._rotation = rotation

        # for convenience, here
        width = self._width
        height = self._height
        rotation = self._rotation

        # Create the ST7789 display object.
        self._disp = st7789.ST7789(
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
        disp = self._disp

        # Create blank image for drawing.
        # Make sure to create image with mode 'RGB' for full color.
        # height = disp.width  # we swap height/width to rotate it to landscape!
        # width = disp.height

        self._image = Image.new("RGB", (width, height))
        image = self._image

        # Get the drawing object so we can draw on it.
        self._draw = ImageDraw.Draw(image)
        disp.image(image, rotation)

        # Create access to the backlight - and turn it on.
        # TODO: OK to turn on backlight by default?
        #
        backlight = digitalio.DigitalInOut(board.D22)
        self._backlight = backlight
        backlight.switch_to_output()
        backlight.value = True

        # Get access to the buttons
        #
        self._buttonA = digitalio.DigitalInOut(board.D23)
        self._buttonA.switch_to_input()
        self._buttonB = digitalio.DigitalInOut(board.D24)
        self._buttonB.switch_to_input()

        self.clearToBlack()

    def getWidth(self):
        return self._width

    def getHeight(self):
        return self._height

    def getDraw(self):
        return self._draw


    def showImageFile(self, imageFilePath, rotation=0):
        """
        Load the indicated file and show it.

        This replaces this object's old image.
        """
        self._rotation = rotation
        with Image.open(imageFilePath) as image:
            self._image = image
            self._draw = ImageDraw.Draw(image)

            self._draw.line((0, 0) + image.size, fill=128)
            self._draw.line((0, image.size[1], image.size[0], 0), fill=128)
            self._draw.rectangle((70, 70, 170, 170), fill=(255,0,0))

            self._disp.image(image, self._rotation)
            print(f"   show: Draw is {self._draw}")
            print(f"   show: Disp is {self._disp}")


    def showImageFileFucked(self, imageFilePath):
        """
        Load the indicated file and display it.
        Supported file types? GIF & PNG are supported; JPEG? others?
        """
        #
        # # Create blank image for drawing.
        # # Make sure to create image with mode 'RGB' for full color.
        if self._disp.rotation % 180 == 90:
            height = self._disp.width  # we swap height/width to rotate it to landscape!
            width = self._disp.height
        else:
            width = self._disp.width
            height = self._disp.height
        # image = Image.new("RGB", (width, height))
        # self.image = image # ???
        #
        # # Get drawing object to draw on image.
        # draw = ImageDraw.Draw(image)
        # self._draw = draw
        #
        # # Draw a black filled box to clear the image.
        # draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
        # self._disp.image(image)
        # self._image = image # ???

        image = Image.open(imageFilePath)
        print("Image opened")

        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width = width
            scaled_height = image.height * width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)
        print("Image resized")

        # Crop and center the image
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))
        self._image = image # ???
        print("Image cropped")

        # how - if at all - can we draw on the image??
        # self.makeAnX()

        # self.draw.line([(0, 0), (width, height)], fill=(255, 0, 0), width=4)

        # Display image.
        self._disp.image(image)
        print("Image displayed")



    def updateImage(self):
        """
        Call this when you have drawn all your stuff.
        """
        self._disp.image(self._image, self._rotation)


    def setBacklight(self, backlightState):
        """
        Set the backlight as indicated.
        """
        self._backlight.value = backlightState


    def clearToBlack(self):
        """
        Clear the LCD display to all black. Does NOT turn off the backlight.
        """
        # Draw a black-filled box to clear the image.
        self._draw.rectangle((0, 0, self._width, self._height), outline=0, fill=(0, 0, 0))
        self._disp.image(self._image, self._rotation)


    #
    # We could do more methods like this... useful? probably not.
    #
    def makeAnX(self):
        w = self._width
        h = self._height
        self._draw.line([(0, 0), (w, h)], fill=(255, 0, 0), width=4)
        self._draw.line([(0, h), (w, 0)], fill=(255, 0, 0), width=4)

        print(f"makeAnX: Draw is {self._draw}")
        print(f"makeAnX: Disp is {self._disp}")

        # these should be equiv ??
        # self.updateImage()
        self._disp.image(self._image, self._rotation)

    def buttonAisPressed(self):
        """
        Get the state of button "A".

        Returns True iff the button is pushed (which is the opposite of the underlying button variable - confusing!)
        Button A is the button attached to GPIO pin 23;
        the right-hand button when you view the display board with the writing at the bottom;
        the upper button if you view the Pi as per the PCB labels.
        """
        return not self._buttonA.value

    def buttonBisPressed(self):
        """
        Get the state of button "B".

        Returns True iff the button is pushed (which is the opposite of the underlying button variable - confusing!)
        Button B is the button attached to GPIO pin 24;
        the left-hand button when you view the display board with the writing at the bottom;
        the lower button if you view the Pi as per the PCB labels.
        """
        return not self._buttonB.value


    def line(self, xy, fill=None, width=0, joint=None):
        self._draw.line(xy, fill, width, joint)

    def rectangle(self, xy, fill=None, outline=None, width=1):
        self._draw.rectangle(xy, fill, outline, width)

    def ellipse(self, xy, fill=None, outline=None, width=1):
        self._draw.ellipse(xy, fill, outline, width)

    def pieslice(self, xy, start, end, fill=None, outline=None, width=1):
        self._draw.pieslice(xy, start, end, fill, outline, width)

    def point(self, xy, fill=None):
        self._draw.point(self, xy, fill)

    def polygon(self, xy, fill=None, outline=None):
        self._draw.polygon(self, xy, fill, outline)

    def regular_polygon(self, bounding_circle, n_sides, rotation=0, fill=None, outline=None):
        self._draw.regular_polygon(self, bounding_circle, n_sides, rotation, fill, outline)

    def rectangle(self, xy, fill=None, outline=None, width=1):
        self._draw.rectangle(self, xy, fill, outline, width)

    def text(self, xy, text, fill=None, font=None, anchor=None, spacing=4, align='left', direction=None,
                features=None, language=None, stroke_width=0, stroke_fill=None, embedded_color=False):
        self._draw.text(self, xy, text, fill, font, anchor, spacing, align, direction,
                    features, language, stroke_width, stroke_fill, embedded_color)

"""
"""
