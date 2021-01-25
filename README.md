# CranPiTFT
A helpful Python library for the Adafruit Raspberry Pi TFT LCD display.

This is an object-oriented wrapper (such as it is) around various bits of code to make
it easier to use the [Adafruit 1.3" TFT LCD display](https://www.adafruit.com/product/4484)
for the Raspberry Pi, in Python3.

Basically it exposes most of the methods of the [Pillow/PIL ImageDraw object](https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html).

For now, it only supports the 1.3" display, which is 240x240, but it should be pretty easy
to modify it for the other similar Adafruit displays based on the ST7789 chipset, such as
the 1.14" display.

For a tutorial on this cool little part, see [Adafruit](https://learn.adafruit.com/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi).

@author robcranfill@robcranfill.net

See the included test/example code for usage examples.
