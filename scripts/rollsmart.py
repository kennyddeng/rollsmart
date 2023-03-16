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
        self.ConsoleLogging = True

        # set up sensor Pins and Addresses
        self.SpeedGPIOA = 27
        self.HeartRateGPIO = 7
        #self.IMUGPIO = 1
        self.LoadCell_dout = 23
        self.LoadCell_sck = 24
        self.LoadCellReferenceUnit = 100
        self.StrainLeftGPIOA = 1
        self.StrainLeftAddress = 0x48
        self.StrainRightGPIOA = 1
        self.StrainRightAddress = 0x69 # need to update with i2c address

        # set up sensor poll rates (seconds per poll)
        #self.SpeedDebounceTime = 0.226 # for max speed 10 km/h
        self.SpeedDebounceTime = 1
        self.HeartRatePollRate = 1
        self.IMUPollRate = 1
        self.LoadPollRate = 1
        self.StrainPollRate = 1

        # speed number of samples per value pushed to database
        self.SpeedSamplesPerValue = 100

        # rollator wheel diameter in metres
        self.WheelDiameter = 0.2

        self.timeStart = 0
        self.timeEnd = 0
        self.updateCounter = 0
        self.intervalSpeed = 0
        self.SpeedCounter = 0

        # connect sensors
        self.connect_sensors()

        # database
        self.firebase = pyrebase.initialize_app(dbconfig.config)
        self.db = self.firebase.database()

        # UPDATE WITH DB ENTRY AND UUID
        self.Entry = "collectedData"
        self.UUID = "userLocalId"

        # threading
        self.running = True

    def run_speed(self):
        '''
        Speed sensor method.
        '''
        while self.running:
            if self.ConsoleLogging:
                print(datetime.now().isoformat(), ": speed sensor detection counter,", self.SpeedCounter)
                print(datetime.now().isoformat(), ": speed sensor value", self.Speed.get_raw_sensor_data())

            if self.Speed.get_raw_sensor_data() == 1:
                if self.SpeedCounter == 0:
                    # start time begins now
                    self.timeStart = time.time()
                    if self.ConsoleLogging: print(datetime.now().isoformat(), ": speed sensor detect start time:", self.timeStart)
                self.SpeedCounter += 1
                if self.ConsoleLogging: print(datetime.now().isoformat(), ": incremented speed sensor detection counter", self.SpeedCounter)

            if self.SpeedCounter == self.SpeedSamplesPerValue:
                # end time begins now
                self.timeEnd = time.time()
                if self.ConsoleLogging: print(datetime.now().isoformat(), ": speed sensor detect end time:", self.timeEnd)

                # calc speed
                self.intervalSpeed = (3.14 * self.WheelDiameter * self.SpeedSamplesPerValue) / (self.timeEnd - self.timeStart)
                if self.ConsoleLogging: print(datetime.now().isoformat(), ": speed sensor interval speed:", self.intervalSpeed, "m/s")

                # push speed to database
                creationDate = datetime.today().strftime('%Y-%m-%d')
                creationTime = datetime.today().strftime('%H:%M:%S')
                self.push_sensor_data_to_database(self.Entry, self.UUID, "speed", creationDate, creationTime, self.intervalSpeed)
                if self.ConsoleLogging: print(datetime.now().isoformat(), ": pushed speed sensor interval speed to database", self.intervalSpeed)

                # reset counter to 0
                self.SpeedCounter = 0
                if self.ConsoleLogging: print(datetime.now().isoformat(), ": speed sensor detection counter reset,", self.SpeedCounter)
            time.sleep(self.SpeedDebounceTime)

    def run_heartrate(self):
        '''
        Heart rate sensor method.
        '''
        while self.running:
            # read sensor data
            red, ir = self.get_raw_sensor_data()
            heartrate_val, hr_valid, sp02, sp02_valid = hrcalc.calc_hr_and_spo2(ir[:100], red[:100])

            # print sensor data
            if self.ConsoleLogging: print(datetime.now().isoformat(), ": heart rate value", heartrate_val)

            # push to database
            creationDate = datetime.today().strftime('%Y-%m-%d')
            creationTime = datetime.today().strftime('%H:%M:%S')
            if hr_valid:
                self.push_sensor_data_to_database(self.Entry, self.UUID, "heartRate", creationDate, creationTime, heartrate_val)
            else:
                invalid_hr = f'{heartrate_val}:{hr_valid}'
                self.push_sensor_data_to_database(self.Entry, self.UUID, "heartRate", creationDate, creationTime, heartrate_val)



            time.sleep(self.HeartRatePollRate)

    def run_imu(self):
        '''
        IMU method.
        '''
        while self.running:
            # read sensor data
            imu_val = self.IMU.get_processed_sensor_data()

            # print sensor data
            if self.ConsoleLogging: print(datetime.now().isoformat(), ": imu value", imu_val)

            # push to database
            creationDate = datetime.today().strftime('%Y-%m-%d')
            creationTime = datetime.today().strftime('%H:%M:%S')
            self.push_sensor_data_to_database(self.Entry, self.UUID, "jerk", creationDate, creationTime, imu_val)

            time.sleep(self.IMUPollRate)

    def run_load(self):
        '''
        Load cell method.
        '''
        while self.running:
            # read sensor data
            loadcell_val = self.LoadCell.get_weight(5)
            self.LoadCell.power_down()
            self.LoadCell.power_up()

            # print sensor data
            if self.ConsoleLogging: print(datetime.now().isoformat(), ": loadcell value", loadcell_val)

            # push to database
            creationDate = datetime.today().strftime('%Y-%m-%d')
            creationTime = datetime.today().strftime('%H:%M:%S')
            self.push_sensor_data_to_database(self.Entry, self.UUID, "seat", creationDate, creationTime, loadcell_val)

            time.sleep(self.LoadPollRate)

    def run_strain(self):
        '''
        Strain gauge method.
        '''
        while self.running:
            # read sensor data
            strain_left_val = self.StrainLeft.get_processed_sensor_data()
            strain_right_val = self.StrainRight.get_processed_sensor_data()


            # print sensor data
            if self.ConsoleLogging: 
                print(datetime.now().isoformat(), ": strain gauge left value", strain_left_val)
                print(datetime.now().isoformat(), ": strain gauge right value", strain_right_val)

            # push to database
            creationDate = datetime.today().strftime('%Y-%m-%d')
            creationTime = datetime.today().strftime('%H:%M:%S')
            self.push_sensor_data_to_database(self.Entry, self.UUID, "weightDistribution", creationDate, creationTime, [strain_left_val, strain_right_val])

            time.sleep(self.StrainPollRate)

    def terminate(self):
        '''
        Terminate running thread.
        '''
        self.running = False

    def connect_sensors(self):
        """
        Initialize, set up, and connect all sensors.

        Sensors connected:
            - Speed
            - HeartRate
            - IMU
            - LoadCell
            - Strain
        """
        self.Speed = Littelfuse59025020(self.SpeedGPIOA)
        self.HeartRate = MaxRefDes117(self.HeartRateGPIO)
        self.IMU = BoschBNO055()
        self.LoadCell = NextionWI1802AX4WI0728(self.LoadCell_dout, self.LoadCell_sck)
        self.LoadCell.set_reading_format("MSB", "MSB")
        self.LoadCell.set_reference_unit(self.LoadCellReferenceUnit)
        self.LoadCell.reset()
        self.LoadCell.tare()
        self.StrainLeft = DaokiBF3503AA(self.StrainLeftGPIOA, self.StrainLeftAddress)
        self.StrainRight = DaokiBF3503AA(self.StrainRightGPIOA, self.StrainRightAddress)

    def push_sensor_data_to_database(self, entry, uuid, datatype, date, time, val):
        """
        Push all sensor data to Firebase database.

            Parameters:
                    entry (str): Database entry type
                    uuid (str): UUID of patient
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

    # heartrate thread
    heartrate = Rollsmart()
    heartrateThread = Thread(target=heartrate.run_heartrate)
    heartrateThread.start()

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
    #heartrate.terminate()
    #imu.terminate()
    #loadstrain.terminate()

