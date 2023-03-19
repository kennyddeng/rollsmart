#!/usr/bin/env python
"""
main device
roll smart :)
"""
import time
import pyrebase
import logging
from rich import print
from rich.logging import RichHandler

from datetime import datetime as dt


import backupDB
import hrcalc
from database import Database
from littelfuse59025020 import Littelfuse59025020
from maxrefdes_117 import MaxRefDes117
from bosch_bno055 import BoschBNO055
from nextionLC import NextionLC
from daoki_bf350_3aa import DaokiBF3503AA


class Rollsmart:
    def __init__(self):
        """
        Constructs all the necessary attributes for the Rollsmart object.
        """
        # Enable or disable console output logging
        self.initialize_cli()

        FORMAT = "%(message)s"
        logging.basicConfig(
            level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
        )
        self.logger = logging.getLogger('Rollsmart')

        # set up sensor Pins and Addresses
        self.speed_gpio_a = 27
        self.heart_rate_gpio = 7
        self.heart_rate_i2c_address = 0x57
        self.imu_gpio = 1
        self.imu_i2c_adress = 0x28
        self.load_cell_dout = 23
        self.load_cell_sck = 24
        self.load_cell_reference_value = 100
        self.strain_left_gpio_a = 1
        self.strain_left_address = 0x48
        #self.strain_right_gpio_a = 2
        #self.strain_right_address = 0x69 # need to update with i2c address

        # set up sensor poll rates (seconds per poll)
        #self.speed_debounce_time = 0.226 # for max speed 10 km/h
        self.speed_debounce_time = 1
        self.heart_rate_poll_rate = 0.75
        self.imu_poll_rate = 1.2
        self.load_poll_rate = 1
        self.strain_poll_rate = 1

        # speed number of samples per value pushed to database
        self.speed_samples_per_value = 100

        # rollator wheel diameter in metres
        self.wheel_diameter = 0.2

        self.speed_interval_time_start = 0
        self.speed_interval_time_end = 0
        self.speed_interval_speed = 0
        self.speed_interval_counter = 0

        # database
        self.db = Database()

        # connect sensors
        self.connect_sensors()
        self.record_sensor_data()


        # db entry and uuid
        self.db_entry = "collectedData"
        self.db_uuid = "userLocalId"

        # threading
        self.running = True

    def terminate(self):
        '''
        Terminate running thread.
        '''
        self.running = False

    def connect_sensors(self):
        """
        Initialize, set up, and connect all sensors.

        Sensors connected:
            - speed
            - heart_rate
            - imu
            - load_cell
            - strain_left
            - strain_right
        """
        self.speed = Littelfuse59025020(self.speed_gpio_a, self.logger)
        self.load_cell = NextionLC()
        self.heart_rate = MaxRefDes117()
        self.imu = BoschBNO055(self.imu_gpio, self.logger)
        self.strain_left = DaokiBF3503AA(self.strain_left_gpio_a, self.strain_left_address)
        #self.strain_right = DaokiBF3503AA(self.strain_right_gpio_a, self.strain_right_address)

    def record_sensor_data(self):
        """
        Function which orchestrates data collection from individual sensors.
        """
        while self.running:
            #check time
            creation_date = datetime.today().strftime('%Y-%m-%d')
            creation_time = datetime.today().strftime('%H:%M:%S')

            # check speed sensor
            speed_val =  self.speed.get_processed_sensor_data()
            self.logger.log(f' Speed sensor: counter = {speed_interval_counter};'
                             ' value = {speed_val}')

            # check load cell
            load_cell_val = self.load_cell.get_processed_sensor_data()
            self.logger.log(f' Load cell: value = {load_cell_val}')

            # check heart rate
            heart_rate_val, hr_valid, sp02, sp02_valid = self.heart_rate.get_processed_sensor_data()
            self.logger.log(f' HeartRate sensor:  HR = {load_cell_val}; '
                            'SP02 = {sp02}; valid = {hr_valid}')

            # check imu
            imu_val = self.imu.get_processed_sensor_data()
            self.imu.log_values(imu_val)

            # check strain gauges
            strain_left_val = self.strain_left.get_processed_sensor_data()
            #strain_right_val = self.strain_right.get_processed_sensor_data()
            self.logger.log(f' Strain Guage: LEFT = {strain_left_val}')
            #self.logger.log(f' Strain Guage: RIGHT = {strain_right_val}')


            # push sensor data
            self.push_sensor_data(self.db_entry, self.db_uuid, "jerk", creation_date, creation_time, imu_val)
            self.push_sensor_data(self.db_entry, self.db_uuid, "seat", creation_date, creation_time, load_cell_val)
            self.push_sensor_data_to_database(self.db_entry, self.db_uuid, "heartRate", creation_date, creation_time, heart_rate_val)
            #self.push_sensor_data_to_database(self.db_entry, self.db_uuid, "weightDistribution", creation_date, creation_time, [strain_left_val, strain_right_val])
            self.push_sensor_data_to_database(self.db_entry, self.db_uuid, "weightDistribution", creation_date, creation_time, strain_left_val)



    def run_speed(self):
        '''
        speed sensor method.
        '''
        while self.running:
            if self.speed.get_raw_sensor_data() == 1:
                if self.speed_interval_counter == 0:
                    # start time begins now
                    self.speed_interval_time_start = time.time()
                    if self.console_logging: print(datetime.now().isoformat(), ": speed sensor detect start time:", self.speed_interval_time_start)
                self.speed_interval_counter += 1
                if self.console_logging: print(datetime.now().isoformat(), ": incremented speed sensor detection counter", self.speed_interval_counter)

            if self.speed_interval_counter == self.speed_samples_per_value:
                # end time begins now
                self.speed_interval_time_end = time.time()
                if self.console_logging: print(datetime.now().isoformat(), ": speed sensor detect end time:", self.speed_interval_time_end)

                # calc speed
                self.speed_interval_speed = (3.14 * self.wheel_diameter * self.speed_samples_per_value) / (self.speed_interval_time_end - self.speed_interval_time_start)
                if self.console_logging: print(datetime.now().isoformat(), ": speed sensor interval speed:", self.speed_interval_speed, "m/s")

                # push speed to database
                creation_date = datetime.today().strftime('%Y-%m-%d')
                creation_time = datetime.today().strftime('%H:%M:%S')
                self.push_sensor_data_to_database(self.db_entry, self.db_uuid, "speed", creation_date, creation_time, self.speed_interval_speed)
                if self.console_logging: print(datetime.now().isoformat(), ": pushed speed sensor interval speed to database", self.speed_interval_speed)

                # reset counter to 0
                self.speed_interval_counter = 0
                if self.console_logging: print(datetime.now().isoformat(), ": speed sensor detection counter reset,", self.speed_interval_counter)
            time.sleep(self.speed_debounce_time)




    def initialize_cli(self):
        """
        Prints CLI welcome message
        """
        print("[deep_sky_blue1 bold]                    _       _                                      _      ")
        print("[deep_sky_blue1 bold]     _ _    ___     | |     | |     ___    _ __    __ _      _ _   | |_   ")
        print("[deep_sky_blue1 bold]    | '_|  / _ \    | |     | |    (_-<   | '  \  / _` |    | '_|  |  _|  ")
        print("[deep_sky_blue1 bold]   _|_|_   \___/   _|_|_   _|_|_   /__/_  |_|_|_| \__,_|   _|_|_   _\__|  ")
        print('[dark_violet] _|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| ')
        print("[dark_violet] "'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-')




if __name__ == '__main__':
    fire.Fire(Rollsmart())
