"""
main device
roll smart :)
"""
import time
import pyrebase
import dbconfig

from littelfuse59025020 import Littelfuse59025020
from maxresdef_117 import MaxResDef117
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

        # set up sensor Pins and Addresses
        self.SpeedGPIOA = 17
        # self.HeartRateGPIO =
        # self.IMUGPIO =
        self.LoadCell_dout = 23
        self.LoadCell_sck = 24
        self.LoadCellReferenceUnit = 1
        self.StrainGPIOA = 1
        self.StrainAddress = 0x48

        # set up sensor poll rates
        self.SpeedPollRate = 420
        self.HeartRatePollRate = 420
        self.IMUPollRate = 420
        self.LoadCellPollRate = 420
        self.StrainPollRate = 420

        # connect sensors
        self.connect_sensors()

        # database
        self.firebase = pyrebase.initialize_app(dbconfig.config)
        self.db = self.firebase.database()

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
        self.HeartRate = MaxResDef117()
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
    rollsmart = Rollsmart()
    while True:
        data = rollsmart.get_sensor_data()
        rollsmart.print_sensor_data(data)
        rollsmart.push_sensor_data_to_database(data, time.strftime("%H:%M:%S", time.localtime()))
        time.sleep(rollsmart.GlobalPollRate)
   