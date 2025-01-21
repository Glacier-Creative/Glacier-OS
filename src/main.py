# Glacier Communicator Firmware
# Main
# By Johnny Stene
print("Glacier Communicatior")
print("Firmware version 0.1-a")

print("Importing drivers")
from sim7600 import CELLULAR
from graphics import GRAPHICS
import time

print("Cell bringup")
cell = CELLULAR()
cell.startup()

print("Graphics bringup")
graphics = GRAPHICS()

print("Home screen start")
home_redraw = True
home_time_last = ""
while True:
    if(home_redraw):
        graphics.draw_image(0, 0, "img/homescreen.xbm")
        graphics.draw_string8x8(16, 24, "Test!")

        graphics.refresh()
        home_redraw = False
    
    cell_status = cell.phone_status()
    print(cell_status)
    if("3" in cell_status):
        graphics.draw_image(0, 0, "img/ring.xbm")
        graphics.refresh()
        cell.answer_call()
        time.sleep(10)
        cell.end_call()
        home_redraw = True