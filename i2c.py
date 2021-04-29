
import smbus
import time
import struct

# objeto clase smbus para i2c
bus = smbus.SMBus(1)
# Direccion del i2c arduino esclavo
address = 0x04

'''
def readLong():
   #number = bus.read_byte(address)
   number=""
   for i in xrange(4):
      number += chr(bus.read_byte(address))
   return struct.unpack('l', number)
'''


def readLong():
   block = bus.read_i2c_block_data(address, 1) #second arg is 'cmd'. It is andatory but not used in this case. It may be used by the higher level protocol
   n=struct.unpack('<l',bytes(block[:4]))[0]
   return n



while True:
    time.sleep(1)
    number = readLong()
    print "[Arduino]", number, "mm"
