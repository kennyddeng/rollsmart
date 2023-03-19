#!/usr/bin/env python
"""
RollSmart Database Interface
"""
import sqlite3
import firebase
import pyrebase
from datetime import datetime as dt

import dbconfig

USER_DATA = "collectedData"
LOGIN_INFO = "loginInfo"
SP02_DATA = "sp02"
HR_DATA = "heartRate"
JERK_DATA = "jerk"
SEAT_DATA = "seat"
SPEED_DATA = "speed"
WEIGHT_DIST_DATA = "weightDistribution"

class Database():
    """
    Class which initializes, pushes and manages Firebase operations for RollSmart
    """
    def __init__(self, logger):
        """
        Initialize Remote and Local databases
        """
        self.logger = logger

        # initialize Firebase cloud database
        self.firebase = pyrebase.initialize_app(dbconfig.config)
        self.db = self.firebase.database()

        # initialize SQLite Local backup database
        self.sqlite_conn = sqlite3.connect('/home/pi/Documents/rollsmart/scripts/localDB.db')
	    self.sqlite_cursor = sqlite_conn.cursor()


    def push_data(self, sensor):
        """
        Wrapper function which establishes which database is available for data pushing.
        If internet is available, data will be pushed using Firebase ortherwise, data is stored
        locally using local SQLite db.

        When internet connection is available, and there is sensor data in local database, data
        will get pushed
        """
        def push_data_wrapper(f):
            def wrapper(*args, **kwargs):
                if self.check_internet_connection():
                    # Check for data backlog in local database
                    if sqlite_cursor.execute("SELECT COUNT(*) FROM sensor_data").fetchone()[0] > 0:
                        data = sqlite_cursor.execute("SELECT * FROM sensor_data").fetchall()
                        self.logger.log('DB: Local data backlog uploaded to Fyrebase')
                        sqlite_cursor.execute("DELETE FROM sensor_data")
                        sqlite_conn.commit()

                    self.db.child(USER_DATA).child(args[0]).child(sensor).child(args[1]).child(args[2]).set(args[3])
                else:
                    push_sqlite(sensor, args[0], args[1], args[2], args[3])
                return f(*args, **kwargs)
            return wrapper
        return push_data_wrapper

    def push_sqlite(self, sensor, uuid, date, time, value):
        """
        Push to sqlite local database
        """
        sqlite_cursor.execute("INSERT INTO sensor_data (sensor_name, value, timestamp, date) VALUES (?, ?, ?, ?)", [sensor, value, time, date])
        sqlite_conn.commit()
        self.logger.log(f"SQLite: stored {sensor}, val:{value}, date: {date}, time: {time}")


    def check_internet_connection(self):
        """
        Check internet connection status
        """
        try:
            requests.get('https://www.google.com')
            internet_status = True
        except:
            internet_status = False

        return internet_status

    @push_data(HR_DATA)
    def add_hr_data(self, uuid, date, time, value):
        """
        Push heart rate data to database

        Args:
            uuid: Unique user idetification
            date: date of measurement ('%Y-%m-%d')
            time: time of measurement ('%H:%M:%S')
            hr: heart rate value to push
        """
        self.logger.log("DB: Pushed HR data to database")

    @push_data(SP02_DATA)
    def add_sp02_data(self, uuid, date, time, sp02):
        """
        Push SP02 data to database

        Args:
            uuid: Unique user idetification
            date: date of measurement ('%Y-%m-%d')
            time: time of measurement ('%H:%M:%S')
            sp02: sp02 value to push
        """
        self.logger.log("DB: Pushed SP02 data to database")

    @push_data(JERK_DATA)
    def add_imu_data(self, uuid, date, time, imu_val):
       """
        Push imu data to database
        "JERK"

        Args:
            uuid: Unique user idetification
            date: date of measurement ('%Y-%m-%d')
            time: time of measurement ('%H:%M:%S')
            imu_val: imu sensor values to push
        """
        self.logger.log("DB: Pushed IMU jerk data to firebase")

    @push_data(SEAT_DATA)
    def add_seat_data(self, uuid, date, time, seat):
        """
        Push seat load cell data to database

        Args:
            uuid: Unique user idetification
            date: date of measurement ('%Y-%m-%d')
            time: time of measurement ('%H:%M:%S')
            seat: seat load cell sensor values to push
        """
        self.logger.log("DB: Pushed seat data to firebase")

    @push_data(SPEED_DATA)
    def add_speed_data(self, uuid, date, time, speed):
        """
        Push speed data to database

        Args:
            uuid: Unique user idetification
            date: date of measurement ('%Y-%m-%d')
            time: time of measurement ('%H:%M:%S')
            seat: seat load cell sensor values to push
        """
        self.db.child(USER_DATA).child(uuid).child(SPEED_DATA).child(date).child(time).set(speed)
        self.logger.log("DB: Pushed speed data to firebase")

    @push_data(WEIGHT_DIST_DATA)
    def add_strain_data(self, uuid, date, time, side):
        """
        Push handlebar strain gauge data to database

        WEIGHT DISTIBUTION
        Args:
            uuid: Unique user idetification
            date: date of measurement ('%Y-%m-%d')
            time: time of measurement ('%H:%M:%S')
            seat: seat load cell sensor values to push
        """
        self.logger.log("DB: Pushed strain gauge weight distribution data to firebase")



if __name__ == '__main__':
    Database()

