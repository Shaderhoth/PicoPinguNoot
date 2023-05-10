from machine import Pin, I2C
import time
import math
from rp2 import PIO, asm_pio




REG_ADD_REG_BANK_SEL                 = 0x7F
REG_VAL_REG_BANK_0                   = 0x00
REG_ADD_PWR_MIGMT_1                  = 0x06
REG_VAL_ALL_RGE_RESET                = 0x80
REG_VAL_RUN_MODE                     = 0x01 # Non low-power mode


class ICM20948(object):
  def __init__(self):
    self.address = 0x68
    self.bus = I2C(1)
    self._write_byte( REG_ADD_PWR_MIGMT_1 , REG_VAL_ALL_RGE_RESET)
    time.sleep(0.1)
    self._write_byte( REG_ADD_PWR_MIGMT_1 , REG_VAL_RUN_MODE)  
    
  def getGyro(self):
    self._write_byte( REG_ADD_REG_BANK_SEL , REG_VAL_REG_BANK_0)
    data =self.bus.readfrom_mem(int(self.address),int(0x2D),12)
    gyrox  = ((data[6]<<8)|data[7])
    if gyrox>=32767:
      gyrox=gyrox-65535
    elif gyrox<=-32767:
      gyrox=gyrox+65535
    return gyrox
  
  def _write_byte(self,cmd,val):
    self.bus.writeto_mem(int(self.address),int(cmd),bytes([int(val)]))
    time.sleep(0.0001)
    
if __name__ == '__main__':
    icm20948=ICM20948()
    while True:
        gyro = icm20948.getGyro()
        print(gyro)
        if (gyro>30000):
            time.sleep(0.1)
    
