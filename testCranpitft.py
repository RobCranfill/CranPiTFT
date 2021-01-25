# Test/examples CranPiTFT
#
from CranPiTFT import CranPiTFT
import time

c = CranPiTFT(rotation=180)
# print(c)
# c.makeAnX()

h = c.height
w = c.width

try:
    for iter in range(10):

        # Using object methods to draw:
        c.line([(0, 0), (w, h)], fill=(255, 0, 0), width=4)
        c.line([(0, h), (w, 0)], fill=(255, 0, 0), width=4)

        balls = iter+1
        k = w/balls
        for i in range(balls):
            c.ellipse([i*k, i*k, (i+1)*k, (i+1)*k], fill=(int(256*i/balls), 0, 256-int(256*i/balls)))

        c.updateImage()

        # Using direct drawing on the ImageDraw object:
        draw = c.draw
        draw.rectangle((50, h-50, 100, h-100), fill=(255,0,0))
        draw.rectangle((w-50, 50, w-100, 100), fill="#FF00FF")

        c.updateImage()

        time.sleep(1)
        c.clearToBlack()
except:
    pass
c.clearToBlack()
c.setBacklight(False)
print("Done")
