import smbus
import time
from scipy.signal import find_peaks
import matplotlib.pyplot as plt

channel = 1
address = 0x48
A0 = 0x40
bus = smbus.SMBus(channel)

'''
while True:
    #print(bus.read_i2c_block_data(address, 0))
    print(bus.read_byte(address))
    time.sleep(1)
'''
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

#while True:
timeout = time.time() + 5
hr = []
while True:
    test = 0
    if test == 5 or time.time() > timeout:
        break
    hr.append(bus.read_byte(address))
    time.sleep(0.1)
    #print(bus.read_byte(address))
    test = test - 1
#peaks = find_peaks(hr, prominence=1)
#print("Peaks position:", peaks[0])
#print(len(peaks[0]))
print(hr)

plt.plot(hr)
#plt.title("Finding Peaks")
#[plt.axvline(p, c='C3', linewidth=0.3) for p in peaks[0]]
plt.show()