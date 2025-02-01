# Glacier Communicator Firmware
# Main
# By Johnny Stene
print("Glacier Communicatior")
print("Firmware version 0.1-a")

print("Importing drivers")
from sim7600 import CELLULAR 
from graphics import GRAPHICS # TODO: GRAPHICS should be Graphics - the hardware driver is DISPLAY and is loaded by graphics.py directly
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
    # TODO: the way this function is designed is kinda terrible... it assumes the state will never be anything other than "ringing" or "in call"
    # ... but even when the caller hangs up before we have the chance to answer it just drops home so maybe fine?
    # TODO: busy waiting in this function will cause infinite loop with it detecting calls... add cell state machine?
    # TODO: hey google what is a state machine?
    print("incoming call")
    graphics.clear()
    graphics.draw_image(0, 0, "img/ring.xbm")
    graphics.draw_string8x8(0, 32, "A: Answer")
    graphics.draw_string8x8(0, 40, "B: End")
    graphics.refresh()

    while True:
        event.publish("busy_wait")
        response = keypad.get_key(wait=False)
        if response == "A":
            cell.answer_call()
            break
        elif response == "B":
            cell.end_call()
            event.publish("home_redraw")
            return
        if not("3" in cell.phone_status()): # 3 is ringing
            event.publish("home_redraw")
            return
        time.sleep(0.05)

    graphics.clear()
    graphics.draw_image(0, 0, "img/in_call.xbm")
    graphics.draw_string8x8(0, 40, "B: End")
    graphics.refresh()
    cell.answer_call()

    while True:
        event.publish("busy_wait")
        response = keypad.get_key(wait=False)
        if response == "B":
            cell.end_call()
            event.publish("home_redraw")
            return
        if not("4" in cell.phone_status()): # 4 is in call
            event.publish("home_redraw")
            return
        time.sleep(0.05)

def handle_sms(**kwargs): # has to be called with data=<msgdata>
    print("incoming sms")
    if not "data" in kwargs: # told you
        print("sms handler error: called without data karg!")
        return

    # TODO: when msg received flag added just trash the whole function and add an unread count
    message = kwargs["data"]
    graphics.clear()
    graphics.draw_image(0, 0, "img/sms.xbm")
    graphics.draw_string8x8(8, 32, db.get_name(message.number))
    graphics.draw_string8x8(8, 40, message.date)
    graphics.draw_string8x8(8, 48, message.time)
    graphics.draw_string8x8(8, 64, message.message)
    graphics.refresh()
    time.sleep(10)

    event.publish("home_redraw")

def busy_wait():
    # TODO: we really need to check for URC from the modem here... phone ringing can screw everything up
    # TODO: state machine for menus/button input? or maybe move housekeeping to an event to be called on loop?

    # check modem status
    cell_status = cell.phone_status()
    if "3" in cell_status: # 3 is ringing
        event.publish("cell_ring")

    # check sms status (probably a better way to do this? can we ask modem for count of REC UNREAD first?)
    messages = cell.read_all_sms()
    for message in messages:
        if message.status == "REC UNREAD":
            db.add_message_entry(message) 
            db.save("db.json") # this will probably never be called more than once per loop so its fine here
            event.publish("cell_sms", data=message) # will probably have to add read flag to messages in the db so we can just have an unread msg count

# subscribe all handlers to their respective events (TODO: rename functions?)
event.subscribe("busy_wait", busy_wait)
event.subscribe("home_redraw", home_redraw)
event.subscribe("cell_ring", handle_call)
event.subscribe("cell_sms", handle_sms)

# Main loop
home_redraw()
while True:
    event.publish("busy_wait")
    
    # app selection will go here eventually
    key_pressed = keypad.get_key(wait=False)