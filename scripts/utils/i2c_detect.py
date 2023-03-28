#!/usr/bin/env python
# pylint: disable=bare-except
"""
Module which connects to i2c bus and checks which devices are connected
"""
import pigpio

def i2c_detect():
    """
    Establish connection to i2c_bus on pi, attempt to connect to each address
    Returns a list of addresses which have a device
    """
    r_pi = pigpio.pi() # connect to local Pi
    connected_devices = []
    for device in range(128):
        address = r_pi.i2c_open(1, device)
        try:
            r_pi.i2c_read_byte(address)
            print(hex(device))
            connected_devices.append(hex(device))
        except: # exception if i2c_read_byte fails
            pass
        r_pi.i2c_close(address)
    r_pi.stop() # disconnect from Pi
    return connected_devices


if __name__ == '__main__':
    i2c_detect()
