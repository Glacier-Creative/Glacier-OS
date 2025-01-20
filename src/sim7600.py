# Glacier Communicator Firmware
# EC25 Cellular Driver
# By Johnny Stene

import machine
import time

class CELLULAR:
    def __init__(self, pin_rx=17, pin_tx=16):
        self.uart = machine.UART(0)
        self.uart.init(115200, tx=machine.Pin(pin_tx), rx=machine.Pin(pin_rx), bits=8, parity=None, stop=1, flow=0)
        self.uart.write("ATE0\r")
        time.sleep(0.1)
        self.uart.read()

    def send_command(self, command, response_timeout=0.5):
        #print("cell >> " + command)
        self.uart.write(command + "\r")
        time.sleep(response_timeout)
        response = self.uart.read().decode("ascii").split("\r\n")[1:-1]
        #print("cell << " + str(response))
        return response
    
    def startup(self):
        self.manufacturer = self.send_command("AT+CGMI")[0]
        self.model = self.send_command("AT+CGMM")[0]
        self.imei = self.send_command("AT+CGSN")[0]
        self.send_command("AT+CMGF=1")

    # NETWORK FUNCTIONS
    def provider_name(self):
        response = self.send_command("AT+CSPN?")[0]
        if(response == "ERROR"):
            return None
        return response[7:-2]

    def imsi(self):
        return self.send_command("AT+CIMI")[0]

    def phone_number(self):
        return self.send_command("AT+CNUM")[0].split("\"")[3]
    
    # CALL FUNCTIONS
    def call(self, number):
        return self.send_command("ATD" + number + ";")
    
    def end_call(self):
        return self.send_command("AT+CHUP")

    def answer_call(self):
        return self.send_command("ATA")

    # SMS FUNCTIONS
    def send_sms(self, number, message):
        response = self.send_command("AT+CMGS=\"" + number + "\"\r")
        response = self.send_command(message + "\x1A", response_timeout=10)
        return response
