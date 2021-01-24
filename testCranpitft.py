# Test/examples CranPiTFT
#
from CranPiTFT import CranPiTFT


c = CranPiTFT()
# print(c)
# c.makeAnX()


h = c.height_
w = c.width_

# using object methods to draw:
c.line([(0, 0), (w, h)], fill=(255, 0, 0), width=4)
c.line([(0, h), (w, 0)], fill=(255, 0, 0), width=4)

for i in range(5):
    c.ellipse([i*50, i*50, (i+1)*50, (i+1)*50], fill=(255, 0, 0))

c.updateImage()

# direct drawing on ImageDraw object:
draw = c.draw_
draw.rectangle((50, h-50, 100, h-100), outline=0, fill=(255,0,0))
draw.rectangle((w-50, 50, w-100, 100), outline=0, fill="#FF00FF")

c.updateImage()

print("Done")
