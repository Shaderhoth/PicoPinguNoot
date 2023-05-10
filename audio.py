import utime
from rp2 import PIO, asm_pio
from machine import Pin

PIN_DATA = 22
PIN_CLOCK = 26
PIN_LRCK = PIN_CLOCK + 1
PIN_BCK = PIN_CLOCK + 2
FREQ = 50000


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
    def __init__(self,smID = 0):
        
        self.PIN_DATA = Pin(PIN_DATA)
        self.PIN_CLOCK = Pin(PIN_CLOCK)
        self.PIN_LRCK = Pin(PIN_LRCK)
        self.PIN_BCK = Pin(PIN_BCK)
        self.smID = smID
        
        self.PIN_DATA.init(Pin.OUT)
        self.PIN_CLOCK.init(Pin.OUT)
        self.PIN_LRCK.init(Pin.OUT)
        self.PIN_BCK.init(Pin.OUT)
        # Create a state machine with the serial number self.smID
        self.sm= rp2.StateMachine(self.smID) 
    
    def write(self):
        #start state machine
        self.sm.init(
            Audio_PIO,
            freq=FREQ * 128,
            out_base = self.PIN_DATA,
            set_base=self.PIN_DATA,
            jmp_pin = self.PIN_DATA,
            sideset_base=self.PIN_CLOCK,
#             out_shiftdir=PIO.SHIFT_RIGHT
            )

        self.sm.active(1)
        for i in range(20000):
            self.sm.put(0)
        for i in range(len(data)/4):
            self.sm.put(((data[i*4]) * 65537)*30)
            self.sm.put(((data[i*4+1]) * 65537)*30)
            #buf[i] = (data[i] - 0x7fff) * 65536 + data[i] - 0x7fff


try:
    Pico_Audio = Audio()
    Pico_Audio.write()

except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))









