# Glacier Communicator Firmware
# Main
# By Johnny Stene

from ec25 import EC25
from graphics import GRAPHICS
import time

print("display amongus")
graphics = GRAPHICS()
for i in range(0, 64):
    graphics.set_pixel(i, 64, 0x00)

graphics.draw_image(0, 0, "img/amogus.xbm")
graphics.draw_image(21, 150, "img/amogus.xbm")
graphics.draw_character8x8(83, 40, "A")
graphics.draw_string8x8(0, 0, "amogus")

graphics.refresh()

print("done")
