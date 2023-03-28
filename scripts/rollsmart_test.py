#!/usr/bin/env python
# pylint: disable=super-with-arguments, too-few-public-methods, invalid-name,
"""
RollSmart Unit Tests
"""
import unittest
try:
    import smbus
except:
    import smbus2 as smbus
from datetime import datetime as dt
from rich import print as pprint
from rich.traceback import install

from utils.init_logger import init_logger
from utils.i2c_detect import i2c_detect
from database import Database
from test_dbconfig import config
from nextionLC import NextionLC
from bosch_bno055 import BoschBNO055
from maxrefdes_117 import MaxRefDes117
from daoki_bf350_3aa import DaokiBF3503AA
from littelfuse59025020 import Littelfuse59025020

install()

USER_DATA = "collectedData"
LOGIN_INFO = "loginInfo"
SP02_DATA = "sp02"
HR_DATA = "heartRate"
JERK_DATA = "jerk"
SEAT_DATA = "seat"
SPEED_DATA = "speed"
WEIGHT_DIST_DATA = "weightDistribution"

class RollsmartTest(unittest.TestCase):
    """
    Class of unit tests to verify the functionality of rollsmart.py
    """
    def __init__(self, *args, **kwargs):
        super(RollsmartTest, self).__init__(*args, **kwargs)
        self.logger = init_logger()
        self.i2c_bus = smbus.SMBus(1)

    def test_connect_database(self):
        """
        Tests connecting to Pyrebase Database solution
        """
        pprint('[bold magenta3] Running test: Connect Database')
        #connect using corect config
        database = Database(self.logger)
        self.assertIsInstance(database, Database)


    def test_connected_sensors(self):
        """
        Test if sensors are actually connected
        """
        sensors = i2c_detect()
        self.assertTrue('0x28' in sensors)
        self.assertTrue('0x57' in sensors)
        self.assertTrue('0x48' in sensors)


    def test_database_upload(self):
        """
        Tests uploading data to database
        """
        pprint('[bold magenta3] Running test: Database upload')
        date = dt.today()

        db = Database(self.logger)
        uuid = "4nIlD4s8Jdc2Uoa1q0DeONmmisH2"
        test_val = 80
        db.add_hr_data(uuid, date, test_val, False)
        stored_val = db.db.child(USER_DATA).child(uuid).child(HR_DATA).child(date).child(time).get()
        self.assertEqual(test_val, stored_val.val())


    def test_hr(self):
        """
        Tests hr data
        """
        pprint('[bold magenta3] Running test: HeartRate & SP02')
        heart_rate = MaxRefDes117(i2c_bus=self.i2c_bus, logger=self.logger)
        hr_val, hr_valid, sp02, sp02_valid = heart_rate.get_processed_sensor_data()
        heart_rate.log_value(hr_val, sp02)
        self.assertIsInstance(heart_rate, MaxRefDes117)


    def test_imu(self):
        """
        Test connecting to bosch_bno055
        """
        pprint('[bold magenta3] Running test: IMU')
        imu = BoschBNO055(logger=self.logger)
        imu_val = imu.get_processed_sensor_data()


    def test_strain_gauge(self):
        """
        Test strain gauge
        """
        pprint('[bold magenta3] Running test: HeartRate & SP02')
        strain_gauge = DaokiBF3503AA(i2c_bus=self.i2c_bus,
                                     gpio=1, address=0x48, logger=self.logger)
        strain_left_val = strain_gauge.get_processed_sensor_data()
        self.assertIsInstance(strain_gauge, DaokiBF3503AA)
        strain_gauge.log_value('left', strain_left_val)

    def test_loadcell(self):
        """
        Test load cell
        """
        pprint('[bold magenta3] Running test: Load Cell')
        load_cell = NextionLC(logger=self.logger)
        load_cell_val = load_cell.get_processed_sensor_data()
        load_cell.log_value(load_cell_val)

class RollsmartTestRunner:
    """
    RollSmart test runner. Runs and records results for all unitTests
    """
    def __init__(self):
        suite = unittest.TestSuite()
        result = unittest.TestResult()
        suite.addTest(unittest.makeSuite(RollsmartTest))
        runner = unittest.TextTestRunner()
        result = runner.run(suite)
        pprint(result.testsRun, result.errors, result.failures)
        self.test_number, self.test_error, self.test_failure = \
                result.testsRun, result.errors, result.failures

if __name__ == '__main__':
    RollsmartTestRunner()
