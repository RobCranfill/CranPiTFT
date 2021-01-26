"""
    Demonstration of use of the CranPiTFT library.
    Draws various shapes. Easy-peasy!
"""
from CranPiTFT import CranPiTFT
import time

c = CranPiTFT(rotation=180)

h = c.height
w = c.width

try:
    for iter in range(10):

        # Using object methods to draw.
        # These are wrappers around the corresponding ImageDraw methods.
        # Be sure to call updateImage() when done.
        #
        c.line([(0, 0), (w, h)], fill=(255, 0, 0), width=4)
        c.line([(0, h), (w, 0)], fill=(255, 0, 0), width=4)

        balls = iter+1
        k = w/balls
        for i in range(balls):
            c.ellipse([i*k, i*k, (i+1)*k, (i+1)*k], fill=(int(256*i/balls), 0, 256-int(256*i/balls)))

        c.updateImage()

        # Using direct drawing on the ImageDraw object.
        # Perhaps a bit faster than the other way?
        #
        # First, get the ImageDraw object, c.draw.
        # Then do as thou wilt with it.
        # Be sure to call updateImage() when done.
        #
        draw = c.draw
        draw.rectangle((50, h-50, 100, h-100), fill=(255,0,0))
        draw.rectangle((w-50, 50, w-100, 100), fill="#FF00FF")

        c.updateImage()

        if c.buttonAisPressed():
            print("Button A pushed - stopping.")
            break

        time.sleep(1)
        c.clearToBlack()
except:
    print("Unexpected error:", sys.exc_info()[0])
    pass
finally:
    c.clearToBlack()
    c.setBacklight(False)
    print("Done")
