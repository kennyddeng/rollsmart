#!/usr/bin/env python
# pylint: disable=super-with-arguments, too-few-public-methods, invalid-name
"""
RollSmart Unit Tests
"""
import unittest
from datetime import datetime as dt
from rich import print as pprint
from rich.traceback import install

from utils.init_logger import init_logger
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

    def test_connect_database(self):
        """
        Tests connecting to Pyrebase Database solution
        """
        pprint('[bold magenta3] Running test: Connect Database')
        #connect using corect config
        database = Database(self.logger)
        self.assertIsInstance(database, Database)

        # connect using bad config
        with self.assertRaises(Exception):
            database = Database(self.logger, config=config)



    def test_database_upload(self):
        """
        Tests uploading data to database
        """
        pprint('[bold magenta3] Running test: Database upload')
        date = dt.today().strftime('%Y-%m-%d')
        time = dt.today().strftime('%H:%M:%S')

        db = Database(self.logger)
        uuid = "4nIlD4s8Jdc2Uoa1q0DeONmmisH2"
        test_val = 80
        db.add_hr_data(uuid, date, time, test_val, False)
        stored_val = db.db.child(USER_DATA).child(uuid).child(HR_DATA).child(date).child(time).get()
        self.assertEqual(test_val, stored_val.val())



    def test_hr(self):
        """
        Tests hr data
        """
        pprint('[bold magenta3] Running test: HeartRate & SP02')


    def test_strain_gauge(self):
        """
        Test strain gauge
        """
        strain_gauge = DaokiBF3503AA(gpio=1, address=0x48, logger=self.logger)
        strain_left_val = strain_gauge.get_processed_sensor_data()
        self.assertIsInstance(strain_gauge, DaokiBF3503AA)
        strain_gauge.log_value('left', strain_left_val)




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
