#!/usr/bin/env python
"""
main device
roll smart :)
"""
import time
import pyrebase
import dbconfig
import backupDB
import hrcalc

from datetime import datetime
from threading import Thread
from littelfuse59025020 import Littelfuse59025020
from maxrefdes_117 import MaxRefDes117
from bosch_bno055 import BoschBNO055
from nextion_wi1802ax4_wi0728 import NextionWI1802AX4WI0728
from daoki_bf350_3aa import DaokiBF3503AA


class Rollsmart:
    def __init__(self):
        """
        Constructs all the necessary attributes for the Rollsmart object.
        """
        # Enable or disable console output logging
        self.console_logging = True

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
        self.heart_rate_poll_rate = 1
        self.imu_poll_rate = 1
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

        # connect sensors
        self.connect_sensors()

        # database
        self.firebase = pyrebase.initialize_app(dbconfig.config)
        self.db = self.firebase.database()

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
        self.speed = Littelfuse59025020(self.speed_gpio_a)
        #self.heart_rate = MaxRefDes117(self.heart_rate_gpio)
        self.heart_rate = MaxRefDes117()
        self.imu = BoschBNO055(self.imu_gpio)
        self.load_cell = NextionWI1802AX4WI0728(self.load_cell_dout, self.load_cell_sck)
        self.load_cell.set_reading_format("MSB", "MSB")
        self.load_cell.set_reference_unit(self.load_cell_reference_value)
        self.load_cell.reset()
        self.load_cell.tare()
        self.strain_left = DaokiBF3503AA(self.strain_left_gpio_a, self.strain_left_address)
        #self.strain_right = DaokiBF3503AA(self.strain_right_gpio_a, self.strain_right_address)

    def run_speed(self):
        '''
        speed sensor method.
        '''
        while self.running:
            if self.console_logging:
                print(datetime.now().isoformat(), ": speed sensor detection counter,", self.speed_interval_counter)
                print(datetime.now().isoformat(), ": speed sensor value", self.speed.get_raw_sensor_data())

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

    def run_heart_rate(self):
        '''
        Heart rate sensor method.
        '''
        while self.running:
            # read sensor data
            heart_rate_val, hr_valid, sp02, sp02_valid = self.heart_rate.get_processed_sensor_data()

            # print sensor data
            if self.console_logging: print(datetime.now().isoformat(), ": heart rate value", heart_rate_val)

            # push to database
            creation_date = datetime.today().strftime('%Y-%m-%d')
            creation_time = datetime.today().strftime('%H:%M:%S')
            if hr_valid:
                self.push_sensor_data_to_database(self.db_entry, self.db_uuid, "heart_rate", creation_date, creation_time, heart_rate_val)
            else:
                invalid_hr = f'{heart_rate_val}:{hr_valid}'
                self.push_sensor_data_to_database(self.db_entry, self.db_uuid, "heart_rate", creation_date, creation_time, heart_rate_val)



            time.sleep(self.heart_rate_poll_rate)

    def run_imu(self):
        '''
        imu method.
        '''
        while self.running:
            # read sensor data
            imu_val = self.imu.get_processed_sensor_data()

            # print sensor data
            if self.console_logging: print(datetime.now().isoformat(), ": imu value", imu_val)

            # push to database
            creation_date = datetime.today().strftime('%Y-%m-%d')
            creation_time = datetime.today().strftime('%H:%M:%S')
            self.push_sensor_data_to_database(self.db_entry, self.db_uuid, "jerk", creation_date, creation_time, imu_val)

            time.sleep(self.imu_poll_rate)

    def run_load(self):
        '''
        Load cell method.
        '''
        while self.running:
            # read sensor data
            load_cell_val = self.load_cell.get_weight(5)
            self.load_cell.power_down()
            self.load_cell.power_up()

            # print sensor data
            if self.console_logging: print(datetime.now().isoformat(), ": load_cell value", load_cell_val)

            # push to database
            creation_date = datetime.today().strftime('%Y-%m-%d')
            creation_time = datetime.today().strftime('%H:%M:%S')
            self.push_sensor_data_to_database(self.db_entry, self.db_uuid, "seat", creation_date, creation_time, load_cell_val)

            time.sleep(self.load_poll_rate)

    def run_strain(self):
        '''
        Strain gauge method.
        '''
        while self.running:
            # read sensor data
            strain_left_val = self.strain_left.get_processed_sensor_data()
            #strain_right_val = self.strain_right.get_processed_sensor_data()


            # print sensor data
            if self.console_logging:
                print(datetime.now().isoformat(), ": strain gauge left value", strain_left_val)
                #print(datetime.now().isoformat(), ": strain gauge right value", strain_right_val)

            # push to database
            creation_date = datetime.today().strftime('%Y-%m-%d')
            creation_time = datetime.today().strftime('%H:%M:%S')
            #self.push_sensor_data_to_database(self.db_entry, self.db_uuid, "weightDistribution", creation_date, creation_time, [strain_left_val, strain_right_val])
            self.push_sensor_data_to_database(self.db_entry, self.db_uuid, "weightDistribution", creation_date, creation_time, strain_left_val)

            time.sleep(self.strain_poll_rate)

    def push_sensor_data_to_database(self, entry, uuid, datatype, date, time, val):
        """
        Push all sensor data to Firebase database.

            Parameters:
                    entry (str): Database entry type
                    uuid (str): db_uuid of patient
                    datatype (str): Name of sensor data type
                    date (str): Calender date
                    time (str): Calender time
                    val (float): Sensor value to be pushed

            Returns:
                    none
        """

        sensor_data = [(datatype, val, time, date)]
        backupDB.uploadData(sensor_data)
        #self.db.child(entry).child(uuid).child(datatype).child(date).child(time).set(val)

if __name__ == '__main__':
    '''
    Instantiate Rollsmart object and separate running threads for each of the sensors.
    '''
    # speed thread
    speed = Rollsmart()
    speedThread = Thread(target=speed.run_speed)
    speedThread.start()

    # heart_rate thread
    heart_rate = Rollsmart()
    heart_rateThread = Thread(target=heart_rate.run_heart_rate)
    heart_rateThread.start()

    # imu thread
    imu = Rollsmart()
    imuThread = Thread(target=imu.run_imu)
    imuThread.start()

    # load thread
    load = Rollsmart()
    loadThread = Thread(target=load.run_load)
    loadThread.start()

    # strain thread
    strain = Rollsmart()
    strainThread = Thread(target=strain.run_strain)
    strainThread.start()

    # terminate threads
    #speed.terminate()
    #heart_rate.terminate()
    #imu.terminate()
    #load.terminate()
    #strain.terminate()

