from epaper import DISPLAY

class GRAPHICS:
    def __init__(self):
        self.display = DISPLAY()
        self.display.init()
        self.display.Clear()

        self.framebuffer = [0xFF for i in range(int(self.display.width * self.display.height / 8))]

    def refresh(self):
        self.display.display(self.framebuffer)
    
    def clear(self, color=0xFF):
        for i in range(int(self.display.width * self.display.height / 8)):
            self.framebuffer[i] = color
    
    def set_pixel(self, x, y, value):
        bit_x = x % 8
        byte_x = x // 8

        if(value):
            self.framebuffer[byte_x + int(y * self.display.width / 8)] &= value | (1<<bit_x)
        else:
            self.framebuffer[byte_x + int(y * self.display.width / 8)] &= value & ~(1<<bit_x)

    def draw_image(self, x, y, filename):
        with open(filename) as file: # Parse XBM file
            contents = file.read()
            width = int(contents.split("\n")[0].split(" ")[2])
            height = int(contents.split("\n")[1].split(" ")[2])
            imgcontent = contents.split("{")[1].replace("};", "").replace(" ", "").replace("\n", "").replace("0x", "").replace(",", "")
            data = bytearray.fromhex(imgcontent)
            
            for iy in range(height):
                for ix in range(width):
                    bit_x = ix % 8
                    byte_x = ix // 8
                    byte_value = data[byte_x + int(iy * width / 8)]
                    bit_value = (byte_value >> (7 - bit_x)) & 1
                    self.set_pixel(x + ix, y + iy, bit_value)