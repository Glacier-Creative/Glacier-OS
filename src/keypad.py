from machine import Pin
import time

class KEYPAD:
    def __init__(self, pins=[28, 27, 26, 22, 21, 20, 19, 18]):
        self.pins = []
        self.translation = [
            ["1", "4", "7", "*"],
            ["2", "5", "8", "0"],
            ["3", "6", "9", "#"],
            ["A", "B", "C", "D"]
        ]
        for pin in range(4):
            self.pins.append(Pin(pins[pin], mode=Pin.OUT))
        
        for pin in range(4):
            self.pins.append(Pin(pins[pin + 4], mode=Pin.IN, pull = Pin.PULL_DOWN))
    
    def get_key(self, wait=False, debounce=False):
        while True:
            for col in range(4):
                self.pins[col].value(1)
                for row in range(4):
                    if self.pins[row + 4].value():
                        # todo: debounce
                        return self.translation[col][row]
                self.pins[col].value(0)
                time.sleep(0.05)

            if wait == False:
                return None