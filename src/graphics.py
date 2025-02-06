from epaper import DISPLAY
import json

class GRAPHICS:
    font24 = [] # TODO: more efficient way to store fonts - this one is like 80kb of ram and we have like 380kb total
    font16 = []

    def __init__(self):
        self.display = DISPLAY()
        self.display.init()

        self.framebuffer = [0xFF for i in range(int(self.display.width * self.display.height / 8))]

        try:
            with open("fonts/24h.json") as fontfile:
                self.font24 = json.load(fontfile)
        except:
            print("Error loading 24h.json")

        try:
            with open("fonts/16h.json") as fontfile:
                self.font16 = json.load(fontfile)
        except:
            print("Error loading 16h.json")

    def refresh(self): # send framebuffer to display
        self.display.display(self.framebuffer)
    
    def clear(self, color=0xFF): # clear display
        for i in range(int(self.display.width * self.display.height / 8)):
            self.framebuffer[i] = color
    
    def set_pixel(self, x, y, value): # set a pixel on display
        # seeing bitwise anything in python makes me sad
        bit_x = 7 - (x % 8)
        byte_x = x // 8

        if value:
            self.framebuffer[byte_x + int(y * self.display.width / 8)] |= (1<<bit_x)
        else:
            self.framebuffer[byte_x + int(y * self.display.width / 8)] &= ~(1<<bit_x)

    def draw_image(self, x, y, filename): # draw an xbm image. hotspots will probably crash this though
        try:
            with open(filename) as file: # Parse XBM file
                print("loading image file " + filename)
                contents = file.read()

                # GIMP at least always exports like this but it isn't 100%... maybe parse the #defines
                width = int(contents.split("\n")[0].split(" ")[2])
                height = int(contents.split("\n")[1].split(" ")[2])
                
                # this will crash the function if what happens above causes problems
                print("size: " + str(width) + "x" + str(height))

                # do evil string manipulation to get the raw bytes... i hate this
                data = bytearray.fromhex(contents.split("{")[1].replace("};", "").replace(" ", "").replace("\n", "").replace("0x", "").replace(",", ""))
                
                # if all somehow went well we should have an image. sanity check the size real quick
                print("image data buffer length: " + str(len(data)))
                if len(data) != width * height / 8:
                    print("image size wrong? (expected " + str(width * height / 8) + ")")
                
                # the bitwise math here is just because xbm image is 1-bit pixels in 8-bit bytes. the angry bitwise magic for writing is in set_pixel
                for iy in range(height):
                    for ix in range(width):
                        bit_x = ix % 8
                        byte_x = ix // 8
                        byte_value = ~data[byte_x + int(iy * width / 8)]
                        bit_value = (byte_value >> (7 - bit_x)) & 1
                        self.set_pixel(x + ix, y + iy, bit_value)
        except:
            print("Something went wrong drawing " + filename)

    def draw_string24h(self, x, y, string): # TODO: add font scaling
        dx = x
        for character in string:
            if(character == " "):
                dx += 8
                continue
            
            width = self.font24[ord(character) - ord("!")][0]
            data = self.font24[ord(character) - ord("!")][1]
            for iy in range(24):
                for ix in range(width):
                    self.set_pixel(dx + ix, y + iy, data[width * iy + ix])
            dx += width
    
    def draw_string16h(self, x, y, string): # TODO: add font scaling
        dx = x
        for character in string:
            if(character == " "):
                dx += 6
                continue
            
            width = self.font16[ord(character) - ord("!")][0]
            data = self.font16[ord(character) - ord("!")][1]
            for iy in range(16):
                for ix in range(width):
                    self.set_pixel(dx + ix, y + iy, data[width * iy + ix])
            dx += width