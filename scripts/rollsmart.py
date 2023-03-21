#!/usr/bin/env python
"""
SYSC4907 Capstone Project Group 33 : RollSmart
Main entry script for Rollsmart
"""
import smbus
from datetime import datetime as dt
import fire
from rich import print as pp
from rich.traceback import install
from utils.init_logger import init_logger
from database import Database
from nextionLC import NextionLC
from bosch_bno055 import BoschBNO055
from maxrefdes_117 import MaxRefDes117
from daoki_bf350_3aa import DaokiBF3503AA
from littelfuse59025020 import Littelfuse59025020


# Initialize Rich Traceback
install()
DB_UUID = "userLocalID"

class Rollsmart:
    """
    Main class which describes Rollsmart Device & dependencies.
    Initializes connection to all required sensors and database. While running,
    the script will poll all the sensors and store data in database.
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self):
        """
        Constructs all the necessary attributes for the Rollsmart object.
        """
        # Enable or disable console output logging
        self.initialize_cli()
        self.logger = init_logger()

        # database
        self.db_ = Database(self.logger)

        # connect sensors
        self.logger.info('Initializing sensors')
        self.i2c_bus = smbus.SMBus(1)
        self.connect_sensors()


        # start recording sensor data
        self.logger.info('[bold] Rollsmart is RUNNING')
        self.running = True
        self.record_sensor_data()


    def connect_sensors(self):
        """
        Initialize, set up, and connect all sensors.

        Sensors connected:
            - speed
            - heart_rate (i2c address = x57, INT = GPIO pin 7)
            - imu (i2c address = x28)
            - load_cell
            - strain_left
            - strain_right
        """
        self.speed = Littelfuse59025020(gpio=27, wheel_diameter=0.2, logger=self.logger)
        self.load_cell = NextionLC(logger=self.logger)
        self.heart_rate = MaxRefDes117(i2c_bus=self.i2c_bus, logger=self.logger)
        self.imu = BoschBNO055(logger=self.logger)
        self.strain_left = DaokiBF3503AA(i2c_bus=self.i2c_bus, gpio=1,
                                         address=0x48, logger=self.logger)
        #self.strain_right = DaokiBF3503AA(gpio=1, address=0x48, logger=self.logger)


    def record_sensor_data(self):
        """
        Function which orchestrates data collection from individual sensors.
        """
        while self.running:
            #check time
            creation_date = dt.today().strftime('%Y-%m-%d')
            creation_time = dt.today().strftime('%H:%M:%S')

            # check speed sensor
            speed_val, _ =  self.speed.get_processed_sensor_data()
            self.speed.log_value(speed_val)

            # check load cell
            load_cell_val = self.load_cell.get_processed_sensor_data()
            self.load_cell.log_value(load_cell_val)

            # check heart rate
            hr_val, hr_valid, sp02, sp02_valid = self.heart_rate.get_processed_sensor_data()
            self.heart_rate.log_value(hr_val, sp02)

            # check imu
            imu_val = self.imu.get_processed_sensor_data()
            self.imu.log_values(imu_val)

            # check strain gauges
            strain_left_val = self.strain_left.get_processed_sensor_data()
            #strain_right_val = self.strain_right.get_processed_sensor_data()
            self.strain_left.log_value('left', strain_left_val)
            #self.strain_right.log_value('right', strain_right_val)

            # push sensor data
            self.db_.add_hr_data(DB_UUID, creation_date, creation_time, hr_val, hr_valid)
            self.db_.add_sp02_data(DB_UUID, creation_date, creation_time, sp02, sp02_valid)
            self.db_.add_imu_data(DB_UUID, creation_date, creation_time, imu_val)
            self.db_.add_seat_data(DB_UUID, creation_date, creation_time, load_cell_val)
            self.db_.add_strain_data(DB_UUID, creation_date, creation_time, strain_left_val)
            self.db_.add_speed_data(DB_UUID, creation_date, creation_time, speed_val)


    def terminate(self):
        """
        Terminate Rollsmart activity
        """
        self.running = False
        self.logger.info('[bold] Rollsmart activity terminated')



    def initialize_cli(self):
        """
        Prints CLI welcome message
        """
        col = 'deep_sky_blue1 bold'
        pp(f"[{col}]                    _       _                                      _      ")
        pp(f"[{col}]     _ _    ___     | |     | |     ___    _ __    __ _      _ _   | |_   ")
        pp(rf"[{col}]    | '_|  / _ \    | |     | |    (_-<   | '  \  / _` |    | '_|  |  _|  ")
        pp(rf"[{col}]   _|_|_   \___/   _|_|_   _|_|_   /__/_  |_|_|_| \__,_|   _|_|_   _\__|  ")
        pp(f'[{col}] _|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""|_|"""""| ')
        pp(f"[{col}] "'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-'"'-O-O-')




if __name__ == '__main__':
    fire.Fire(Rollsmart())
