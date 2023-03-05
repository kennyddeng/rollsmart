"""
Reed Switch
"""
import time

import RPi.GPIO as GPIO

class Littelfuse59025020():
    def __init__(self, gpioA):
        self.gpioChannelA = gpioA

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpioChannelA, GPIO.IN)

    def get_raw_sensor_data(self):
        # read sensor data from pins
        return GPIO.input(self.gpioChannelA)
