"""
    Demonstration of use of the CranPiTFT library.

    Based on Adafruit's example code at
     https://learn.adafruit.com/adafruit-mini-pitft-135x240-color-tft-add-on-for-raspberry-pi/python-stats
"""
from CranPiTFT import CranPiTFT
from PIL import ImageFont
import time
import subprocess


c = CranPiTFT(0)

# Load a TrueType Font.
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("DejaVuSans.ttf", 24)

# Turn on the backlight
c.setBacklight(True)

try:
    while True:

        # Draw a black-filled box to clear the image.
        c.draw.rectangle((0, 0, c.width, c.height), outline=0, fill=0)

        # Shell scripts for system monitoring from here:
        # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
        cmd = "hostname -I | cut -d' ' -f1"
        IP = "IP: " + subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
        CPU = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
        MemUsage = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
        Disk = subprocess.check_output(cmd, shell=True).decode("utf-8")
        cmd = "cat /sys/class/thermal/thermal_zone0/temp |  awk '{printf \"CPU Temp: %.1f C\", $(NF-0) / 1000}'"  # pylint: disable=line-too-long
        Temp = subprocess.check_output(cmd, shell=True).decode("utf-8")

        # Write four lines of text.
        x = 0
        y = -2
        c.draw.text((x, y), IP, font=font, fill="#FFFFFF")

        y += font.getsize(IP)[1]
        c.draw.text((x, y), CPU, font=font, fill="#FFFF00")

        y += font.getsize(CPU)[1]
        c.draw.text((x, y), MemUsage, font=font, fill="#00FF00")

        y += font.getsize(MemUsage)[1]
        c.draw.text((x, y), Disk, font=font, fill="#0000FF")

        y += font.getsize(Disk)[1]
        c.draw.text((x, y), Temp, font=font, fill="#FF00FF")

        # Display image.
        c.updateImage()
        time.sleep(0.1)
except:
    pass

c.clearToBlack()
c.setBacklight(False)
