# Glacier Communicator Firmware
# Main
# By Johnny Stene

from ec25 import EC25
from graphics import GRAPHICS
import time

print("display amongus")
graphics = GRAPHICS()

graphics.draw_image(0, 0, "img/homescreen.xbm")
graphics.draw_image(0, 0, "img/amogus.xbm")
graphics.draw_image(32, 0, "img/bat_empty.xbm")

graphics.draw_image(0, 216, "img/app_empty.xbm")

graphics.draw_string8x8(0, 0, "amogus")

graphics.refresh()

print("done")
