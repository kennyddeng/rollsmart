import smbus
import time
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

channel = 1
address = 0x48
A0 = 0x40
bus = smbus.SMBus(channel)


while True:
    #print(bus.read_i2c_block_data(address, 0))
    print(bus.read_byte(address))
    time.sleep(1)

'''
while True:
    #bus.write_byte(address,A0)
    write = bus.write_byte_data(address, A0, 0)
    read = bus.read_byte(address)
    #value = bus.read_byte(address)
    print(read)
    #print(bus.read_i2c_block_data(address, 0))
    time.sleep(0.1)
'''

