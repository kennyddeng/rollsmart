"""
main device
roll smart :)
"""
import time
import pyrebase
import dbconfig

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
        # set up global poll rate
        self.GlobalPollRate = 0.5

        # Enable or disable console output logging
        self.ConsoleLogging = True

        # set up sensor Pins and Addresses
        self.SpeedGPIOA = 17
        # self.HeartRateGPIO =
        # self.IMUGPIO =
        self.LoadCell_dout = 23
        self.LoadCell_sck = 24
        self.LoadCellReferenceUnit = 1
        self.StrainGPIOA = 1
        self.StrainAddress = 0x48

        # set up sensor poll rates (seconds per poll)
        self.SpeedPollRate = 1
        self.HeartRatePollRate = 420
        self.IMUPollRate = 420
        self.LoadCellPollRate = 5
        self.StrainPollRate = 5

        # speed debouncing time in seconds
        self.SpeedDebounceTime = 0.5

        # speed number of samples per value
        self.SpeedSamplesPerValue = 10

        # rollator wheel diameter in metres
        self.WheelDiameter = 0.4

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

        # threading
        self.running = True

    def run_speed(self):
        #self.Speed.dont_stop()
        while self.running:
            if self.ConsoleLogging: print(datetime.now().isoformat(), ": speed sensor detection counter,", self.SpeedCounter)
            if self.ConsoleLogging: print(datetime.now().isoformat(), ": speed sensor value", self.Speed.get_raw_sensor_data())
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
                if self.ConsoleLogging: print(datetime.now().isoformat(), ": speed sensor interval speed:", self.intervalSpeed)
                # push speed to database
                creationDate = datetime.today().strftime('%Y-%m-%d')
                creationTime = datetime.today().strftime('%H:%M:%S')
                self.db.child("collectedData").child("userLocalId").child("speed").child(creationDate).child(creationTime).set(self.intervalSpeed)
                if self.ConsoleLogging: print(datetime.now().isoformat(), ": pushed speed sensor interval speed to database", self.intervalSpeed)
                # reset counter to 0
                self.SpeedCounter = 0
                if self.ConsoleLogging: print(datetime.now().isoformat(), ": speed sensor detection counter reset,", self.SpeedCounter)
            time.sleep(self.SpeedPollRate)

    def run_other(self):
        while self.running:
            otherSensorData = self.get_other_sensor_data()
            if self.ConsoleLogging: print(datetime.now().isoformat(), ": other sensors values", otherSensorData)

            # push speed to database
            creationDate = datetime.today().strftime('%Y-%m-%d')
            creationTime = datetime.today().strftime('%H:%M:%S')
            self.db.child("collectedData").child("userLocalId").child("heartRate").child(creationDate).child(creationTime).set(otherSensorData[0])
            self.db.child("collectedData").child("userLocalId").child("jerk").child(creationDate).child(creationTime).set(otherSensorData[1])
            self.db.child("collectedData").child("userLocalId").child("seat").child(creationDate).child(creationTime).set(otherSensorData[2])
            self.db.child("collectedData").child("userLocalId").child("weightDistribution").child(creationDate).child(creationTime).set(otherSensorData[3])
            
            time.sleep(self.StrainPollRate)

    def terminate(self):
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
        self.Speed = Littelfuse59025020(self.SpeedGPIOA, self.SpeedSamplesPerValue, self.WheelDiameter)
        self.HeartRate = MaxRefDes117()
        self.IMU = BoschBNO055()
        self.LoadCell = NextionWI1802AX4WI0728(self.LoadCell_dout, self.LoadCell_sck)
        self.LoadCell.set_reading_format("MSB", "MSB")
        self.LoadCell.set_reference_unit(self.LoadCellReferenceUnit)
        self.LoadCell.reset()
        self.LoadCell.tare()
        self.Strain = DaokiBF3503AA(self.StrainGPIOA, self.StrainAddress)

    def poll_sensors(self):
        """
        Polls all sensors for current processed sensor data and initializes as parameter variable.

        Sensors polled: 
            - Speed
            - HeartRate
            - IMU
            - LoadCell
            - Strain
        """
        self.speed = self.Speed.get_processed_sensor_data()
        self.heartrate = self.HeartRate.get_processed_sensor_data()
        self.imu = self.IMU.get_processed_sensor_data()
        self.loadcell = self.LoadCell.get_weight(5)
        self.LoadCell.power_down()
        self.LoadCell.power_up()
        self.strain = self.Strain.get_processed_sensor_data()

    def get_sensor_data(self):
        """
        Polls all sensors for current data and returns all values in a list.

            Returns: 
                (list): [speed, heartrate, imu, loadcell, strain]
        """
        self.poll_sensors()
        return [self.speed, self.heartrate, self.imu, self.loadcell, self.strain]

    def get_other_sensor_data(self):
        """
        Polls all sensors other then speed for current data and returns all values in a list.

            Returns: 
                (list): [heartrate, imu, loadcell, strain]
        """
        self.poll_sensors()
        return [self.heartrate, self.imu, self.loadcell, self.strain]
    
    def print_sensor_data(self, data):
        """
        Prints all current polled sensor data.
        """
        print(data)

    def push_sensor_data_to_database(self, data, time):
        """
        Push all sensor data to Firebase database.

            Parameters:
                    data (list): A list of sensor data
                    time (str): Current time in String format

            Returns:
                    none
        """
        data = self.get_sensor_data()
        self.db.child("collectedData").child("UUID").child("speed").child(time).set(data[0])
        self.db.child("collectedData").child("UUID").child("heartrate").child(time).set(data[1])
        self.db.child("collectedData").child("UUID").child("imu").child(time).set(data[2])
        self.db.child("collectedData").child("UUID").child("loadcell").child(time).set(data[3])
        self.db.child("collectedData").child("UUID").child("strain").child(time).set(data[4])
        
if __name__ == '__main__':
    speed = Rollsmart()
    speedThread = Thread(target=speed.run_speed)
    speedThread.start()

    other = Rollsmart()
    otherThread = Thread(target=other.run_other)
    otherThread.start()

    # terminate threads
    #speed.terminate()
    #other.terminate()
   