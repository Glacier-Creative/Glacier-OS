# Glacier Communicator Firmware
# Main
# By Johnny Stene
print("Glacier Communicatior")
print("Firmware version 0.1-a")

print("Importing drivers")
from sim7600 import CELLULAR
from graphics import GRAPHICS
from keypad import KEYPAD
from event import EventSystem
from database import Database
import time

print("Start event system")
event = EventSystem()

print("Load database")
db = Database()
db.load("db.json")

print("Keypad bringup")
keypad = KEYPAD()

print("Cell bringup")
cell = CELLULAR()
cell.startup()

print("Graphics bringup")
graphics = GRAPHICS()

def home_redraw():
    graphics.draw_image(0, 0, "img/homescreen.xbm")
    graphics.draw_string8x8(16, 24, "Test!")
    graphics.refresh()

def handle_call():
    print("incoming call")
    graphics.clear()
    graphics.draw_image(0, 0, "img/ring.xbm")
    graphics.draw_string8x8(0, 32, "A: Answer")
    graphics.draw_string8x8(0, 40, "B: End")
    graphics.refresh()
    while True:
        response = keypad.get_key(wait=False)
        if(response == "A"):
            cell.answer_call()
            break
        elif(response == "B"):
            cell.end_call()
            return
        if not("3" in cell.phone_status()):
            return
        time.sleep(0.05)

    graphics.clear()
    graphics.draw_image(0, 0, "img/in_call.xbm")
    graphics.draw_string8x8(0, 40, "B: End")
    graphics.refresh()
    cell.answer_call()

    while True:
        response = keypad.get_key(wait=False)
        if(response == "B"):
            cell.end_call()
            return
        if not("4" in cell.phone_status()):
            return
        time.sleep(0.05)

def handle_sms(**kwargs):
    print("incoming sms")
    if not "data" in kwargs:
        print("sms handler error: called without data karg!")
        return

    message = kwargs["data"]
    graphics.clear()
    graphics.draw_image(0, 0, "img/sms.xbm")
    graphics.draw_string8x8(8, 32, message.number)
    graphics.draw_string8x8(8, 40, message.date)
    graphics.draw_string8x8(8, 48, message.time)
    graphics.draw_string8x8(8, 64, message.message)
    graphics.refresh()
    time.sleep(10)

event.subscribe("home_redraw", home_redraw)
event.subscribe("cell_ring", handle_call)
event.subscribe("cell_sms", handle_sms)

# Main loop
home_redraw()
while True:
    cell_status = cell.phone_status()
    if "3" in cell_status:
        event.publish("cell_ring")
        event.publish("home_redraw")

    messages = cell.read_all_sms()
    for message in messages:
        if(message.status == "REC UNREAD"):
            db.add_message_entry(message)
            event.publish("cell_sms", data=message)
            event.publish("home_redraw")
    
    key_pressed = keypad.get_key(wait=False)