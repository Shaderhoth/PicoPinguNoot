from machine import Pin, I2C
import time
import math
from rp2 import PIO, asm_pio


FREQ = 54000
data = open("pingu.pcm", "rb").read()

@asm_pio(out_init=PIO.OUT_LOW, sideset_init=(PIO.OUT_LOW, PIO.OUT_LOW), autopull=True)
def Audio_PIO():
    set(x, 14)            .side(0b10)
    
    label("bitloop1")
    nop()                 .side(0b11)  
    out(pins, 1)          .side(0b10)
    nop()                 .side(0b11)  
    jmp(x_dec,"bitloop1") .side(0b10)
    set(x, 15)            .side(0b11)
    
    label("bitloop0")  
    out(pins, 1)          .side(0b00)
    nop()                 .side(0b01)
    nop()                 .side(0b00)
    jmp(x_dec,"bitloop0") .side(0b01)
    out(pins, 1)          .side(0b10)
    nop()                 .side(0b11)    
    

class Audio:
    def __init__(self):
        
        self.PIN_DATA = Pin(22)
        self.PIN_CLOCK = Pin(26)
        
        self.PIN_DATA.init(Pin.OUT)
        self.PIN_CLOCK.init(Pin.OUT)
        self.sm= rp2.StateMachine(0)
        
        self.sm.init(
            Audio_PIO,
            freq=FREQ * 128,
            out_base = self.PIN_DATA,
            set_base=self.PIN_DATA,
            jmp_pin = self.PIN_DATA,
            sideset_base=self.PIN_CLOCK)

        self.sm.active(1)
    
    def write(self):
        for i in range(20000):
            self.sm.put(0)
        for i in range(len(data)/4):
            self.sm.put(((data[i*4]) * 65537)*30)
            self.sm.put(((data[i*4+1]) * 65537)*30)

if __name__ == '__main__':
    Pico_Audio = Audio()
    while True:
        gyro = 100000
        if (gyro>30000):
            Pico_Audio.write()
            time.sleep(0.1)
    
