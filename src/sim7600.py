# Glacier Communicator Firmware
# EC25 Cellular Driver
# By Johnny Stene

import machine
import time

class SMS_MESSAGE:
    def __init__(self, status, number, date, time, message):
        self.status = status
        self.number = number
        self.date = date
        self.time = time
        self.message = message

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
        try:
            response = self.uart.read().decode("ascii").split("\r\n")[1:-1]
        except:
            print("No response from modem!!!!")
        #print("cell << " + str(response))
        return response
    
    def startup(self):
        self.manufacturer = self.send_command("AT+CGMI")[0]
        self.model = self.send_command("AT+CGMM")[0]
        self.imei = self.send_command("AT+CGSN")[0]
        self.send_command("AT+CMGF=1")
        self.send_command("AT+CTZU=1")

    def get_rtc(self):
        response = self.send_command("AT+CCLK?")
        for line in response:
            if("+CCLK" in line):
                return line.split("\"")[1]
        return None

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
    
    def phone_status(self):
        # 0: ready
        # 3: ringing
        # 4: in call
        return self.send_command("AT+CPAS")[0].split(" ")[1]

    # SMS FUNCTIONS
    def send_sms(self, number, message):
        response = self.send_command("AT+CMGS=\"" + number + "\"\r")
        response = self.send_command(message + "\x1A", response_timeout=10)
        return response

    def read_all_sms(self):
        response = self.send_command("AT+CMGL=\"ALL\"", response_timeout=1)
        messages = []
        for i in range(int(len(response) / 2)):
            mi = i * 2
            metadata = response[mi].replace("\"", "").split(",")
            if(len(metadata) == 6):
                message = SMS_MESSAGE(metadata[1], metadata[2], metadata[4], metadata[5], response[mi + 1])
                messages.append(message)
        return messages