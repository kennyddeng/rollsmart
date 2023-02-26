"""
Reed Switch
"""
import time

import RPi.GPIO as GPIO

class Littelfuse59025020():
    def __init__(self, gpioA, numSamples, wheelDia):
        self.gpioChannelA = gpioA
        self.numberOfSamplesPerValue = numSamples
        self.WheelDiameter = wheelDia

        self.timeStart = 0
        self.timeEnd = 0
        self.updateCounter = 0
        self.intervalSpeed = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpioChannelA, GPIO.IN)

    def get_raw_sensor_data(self):
        # read sensor data from pins
        return GPIO.input(self.gpioChannelA)
    
    def get_processed_sensor_data(self):
         # process raw sensor data into something useful to read
        raw = self.get_raw_sensor_data()
        return raw*10
    
    def updateSpeed(self, start, end):
        self.intervalSpeed = (end - start) / self.WheelDiameter
    
    def update_start_end_times(self):
        if self.updateCounter == 0: # start timer
            self.timeStart = time.time()
            self.updateCounter += 1
        elif self.updateCounter == self.numberOfSamplesPerValue: # end timer
            self.timeEnd = time.time()
            self.updateCounter = 0
            self.updateSpeed(self.timeStart, self.timeEnd)
        else:
            self.updateCounter += 1