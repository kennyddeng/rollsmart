"""
Reed Switch
"""
import time

import RPi.GPIO as GPIO

class Littelfuse59025020():
    def __init__(self, gpioA, wheel_diameter, logger):
        self.gpioChannelA = gpioA
        self.wheel_diameter = wheel_diameter
        self.logger = logger


        self.speed_interval_time_start = 0
        self.speed_interval_time_end = 0
        self.speed_interval_counter = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpioChannelA, GPIO.IN)

    def get_raw_sensor_data(self):
        # read sensor data from pins
        return GPIO.input(self.gpioChannelA)

    def get_processed_sensor_data(self):
        """
        Return processed speed sensor data
        """
        if self.get_raw_sensor_data() == 1:
            if self.speed_interval_counter == 0:
                # start time begins now
                self.speed_interval_time_start = time.time()
                self.logger.log(f'speed detection initiated @ {speed_interval_time_start}')
            self.speed_interval_counter += 1
            self.logger.log(f'incremented speed sensor counter: value = {speed_interval_counter}')

        if self.speed_interval_counter == self.speed_samples_per_value:
                # end time begins now
            self.speed_interval_time_end = time.time()
            self.logger.log(f'speed detection terminated @ {speed_interval_time_end}')

            # calc speed
            measurement_duration = self.speed_interval_time_start - self.speed_interval_time_end
            measurement_interval_speed = (3.14 * self.wheel_diameter * self.speed_samples_per_value) / measurement_duration
            # reset counter to 0
            self.speed_interval_counter = 0
            self.logger.log('Speed sensor counter RESET')

        return measurement_interval_speed

