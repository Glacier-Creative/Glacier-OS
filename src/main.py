# Glacier Communicator Firmware
# Main
# By Johnny Stene

from sim7600 import CELLULAR
from graphics import GRAPHICS
import time

cell = CELLULAR()
cell.startup()
print(cell.provider_name())
print(cell.imsi())
#print(cell.send_command("AT+CMGS=\"17805049202\"\rTest\x1A"))

print("display amongus")
graphics = GRAPHICS()

graphics.draw_image(0, 0, "img/homescreen.xbm")
graphics.draw_image(0, 0, "img/amogus.xbm")
graphics.draw_image(32, 0, "img/bat_empty.xbm")

graphics.draw_image(0, 216, "img/app_empty.xbm")

graphics.draw_string8x8(0, 38, cell.manufacturer)
graphics.draw_string8x8(0, 46, cell.model)
graphics.draw_string8x8(0, 54, cell.imei)

graphics.refresh()

print("done")
