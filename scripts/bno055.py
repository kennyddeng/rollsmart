#!/usr/bin/env python
"""
Script which interfaces with BNO555 IMU sensor
"""
import time
import adafruit_bno055
from adafruit_extended_bus import ExtendedI2C as I2C
from datetime import datetime as dt

class BNO055():
    """
    Class to interface with BNO055 IMU sensor
    """
    def __init__(self):
        """
        Initialize connection to BNO555
        """
        self.i2c = I2C(1) #use ls /dev/i2c to see i2c devices connected and which port is bno055
        self.sensor = adafruit_bno055.BNO055_I2C(i2c)

    def query(self):
        """
        Query BNO055 for all 9 available datapoints

        Returns:
            data [9x1 array] : Contains real time, along with 9 values queries from sensor
                1) UTC Time Stamp
                2) Temperature (dec C)
                3) Accelerometer (m/s^2)
                4) Magnetometer (microteslas)
                5) Gyroscope (rad/sec)
                6) Euler angle
                7) Quaternion
                8) Linear acceleration (m/s^2)
                9) Gravity (m/s^2)
        """
        time = dt.utcnow()
        temperature = self.sensor.temperature
        acceleration = self.sensor.acceleration
        magnetic = self.sensor.magnetic
        gyro = self.sensor.gyro
        euleur = self.sensor.euler
        quaternion = self.sensor.quaternion
        linear_acceleration = self.sensor.linear_acceleration
        gravity = self.sensor.gravity

        return [time, acceleration, magnetic, gyro, euler, quaternion, linear_acceleration, gravity]

    def print_query(self, measurement_freq=1):
        """
        Dev function which prints out values of BNO055 at desired interval

        Input:
            measurement_freq [int]: Desired frequency of interval measurement in seconds
                (Default = 1sec)
        """
        while True:
            query = self.query()
            print("Time: {} degrees C".format(query[0])
            print("Temperature: {} degrees C".format(query[1])
            print("Accelerometer (m/s^2): {}".format(query[2]))
            print("Magnetometer (microteslas): {}".format(query[3]))
            print("Gyroscope (rad/sec): {}".format(queyr[4]))
            print("Euler angle: {}".format(query[5]))
            print("Quaternion: {}".format(query[6]))
            print("Linear acceleration (m/s^2): {}".format(query[7]))
            print("Gravity (m/s^2): {}".format(query[8]))
            print()

            time.sleep(measurement_freq)

if __name__ == '__main__':
    BNO055()

