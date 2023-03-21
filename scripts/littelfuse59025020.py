#!/usr/bin/env python3
# pylint: disable=invalid-name, logging-fstring-interpolation, broad-exception-caught
"""
Reed Switch
"""
import time
try:
    from RPi import GPIO
except ImportError:
    from FakeRPi import GPIO


class Littelfuse59025020():
    """
    Class which interfaces with LittelFuse Reed switch speed sensor

    Args:
        gpio: gpio address on Raspberry Pi
        wheel_diameter: diameter of rollator wheel for speed calculation
        logger: logging object from top module
    """
    def __init__(self, gpio, wheel_diameter, logger):
        self.gpio_channel_a = gpio
        self.wheel_diameter = wheel_diameter
        self.logger = logger

        # speed number of samples per value pushed to database
        self.speed_samples_per_value = 100
        self.speed_interval_time_start = 0
        self.speed_interval_time_end = 0
        self.speed_interval_counter = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.gpio_channel_a, GPIO.IN)

    def get_raw_sensor_data(self):
        """
        read sensor data from pins
        """
        return GPIO.input(self.gpio_channel_a)

    def get_processed_sensor_data(self):
        """
        Return processed speed sensor data
        """
        measurement_duration = 0
        if self.get_raw_sensor_data() == 1:
            if self.speed_interval_counter == 0:
                # start time begins now
                self.speed_interval_time_start = time.time()
                self.logger.info(f'speed detection initiated @ {self.speed_interval_time_start}')
            self.speed_interval_counter += 1
            self.logger.info('incremented speed sensor counter: value'
                            f' = {self.speed_interval_counter}')


        if self.speed_interval_counter == self.speed_samples_per_value:
                # end time begins now
            self.speed_interval_time_end = time.time()
            self.logger.info(f'speed detection terminated @ {self.speed_interval_time_end}')

            # calc speed
            measurement_duration = self.speed_interval_time_start - self.speed_interval_time_end
            measurement_interval_speed = (3.14 * self.wheel_diameter *
                                          self.speed_samples_per_value) / measurement_duration
            # reset counter to 0
            self.speed_interval_counter = 0
            self.logger.info('Speed sensor counter RESET')

        else:
            measurement_interval_speed = False
            self.log_value(message='Unable to determine speed of Rollsmart')

        return measurement_interval_speed, self.speed_interval_counter

    def log_value(self, speed_val=None, message=None):
        """
        Return Rich formatted logging message for speed value
        """
        log_col = '[bold dark_turquoise]'
        value_col = '[turquoise4]'
        if message is not None:
            self.logger.warning(f'{log_col}SPEED (LittelFuse)[/]: {value_col}{message}[/]')
        else:
            self.logger.info(f'{log_col}SPEED (LittelFuse)[/]: value={value_col}{speed_val}[/]')
