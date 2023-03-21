#!/usr/bin/env python
# pylint: disable=unused-argument, bare-except, invalid-name, too-many-arguments, no-self-argument
"""
RollSmart Database Interface
"""
import functools
import sqlite3
import requests
import pyrebase
from utils.init_logger import init_logger
import dbconfig

USER_DATA = "collectedData"


class Database():
    """
    Class which initializes, pushes and manages Firebase operations for RollSmart

    Args:
        logger = Top module logger
        config = database config
    """
    def __init__(self, logger, config=None):
        """
        Initialize Remote and Local databases
        """
        self.logger = logger or init_logger()
        self.config = config or dbconfig.config

        # initialize Firebase cloud database
        self.logger.info('Initializing database connections')
        self.firebase = pyrebase.initialize_app(self.config)
        self.db = self.firebase.database()

        # initialize SQLite Local backup database
        self.sqlite_conn = sqlite3.connect('localDB.db')
        self.sqlite_cursor = self.sqlite_conn.cursor()


    def push_data(sensor):
        """
        Wrapper function which establishes which database is available for data pushing.
        If internet is available, data will be pushed using Firebase ortherwise, data is stored
        locally using local SQLite db.

        When internet connection is available, and there is sensor data in local database, data
        will get pushed

        Args:
            sensor: sensor database key
        """
        def push_data_wrapper(func):
            @functools.wraps(func)
            def wrapper(self, *args, **kwargs):
                try:
                    self.check_internet_connection()
                    # push new sensor data
                    self.push_firebase(sensor=sensor, uuid=args[0], date=args[1],
                                       time=args[2], value=args[3])

                    # check for data backlog in local database
                    backlog_data = self.sqlite_cursor.execute("SELECT COUNT(*) FROM sensor_data")
                    if backlog_data.fetchone()[0] > 0:
                        self.logger.info(f'[bold]DB (Firebase)[/]: Found backlog {sensor} data')
                        data = backlog_data.fetchall()
                        self.sqlite_cursor.execute("DELETE FROM sensor_data")
                        self.sqlite_conn.commit()
                        for d in data:
                            self.push_firebase(sensor=d[0], uuid=args[0], date=d[3],
                                               time=args[2], value=d[1])
                except ConnectionError:
                    self.push_sqlite(sensor, args[0], args[1], args[2], args[3])

                return func(self, *args, **kwargs)
            return wrapper
        return push_data_wrapper


    def push_sqlite(self, sensor, uuid, date, time, value):
        """
        Push to sqlite local database
        """
        self.sqlite_cursor.execute("INSERT INTO sensor_data (sensor_name, value, timestamp, date)"
                                   " VALUES (?, ?, ?, ?)", [sensor, value, time, date])
        self.sqlite_conn.commit()
        self.logger.info(f'[bold]DB (SQLite) - {sensor}: Pushed {value}')


    def push_firebase(self, sensor, uuid, date, time, value):
        """
        Push to firebase cloud database
        Args:
            sensor: sensor name
            uuid: unique user identifier token
            date: date of measurement
            time: time of measurement
            value: value to be stored
        """
        self.db.child(USER_DATA).child(uuid).child(sensor).child(date).child(time).set(value)
        self.logger.info(f'[bold]DB (Firebase) - {sensor}[/]: Pushed {value}')


    def check_internet_connection(self):
        """
        Check internet connection status
        """
        try:
            requests.get('https://www.google.com', timeout=1)
        except ConnectionError as exec:
            raise ConnectionError from exec


    @push_data('heartRate')
    def add_hr_data(self, uuid, date, time, hr, hr_valid):
        """
        Push heart rate data to database

        Args:
            uuid: Unique user idetification
            date: date of measurement ('%Y-%m-%d')
            time: time of measurement ('%H:%M:%S')
            hr: heart rate value to push
            hr_valid (bool): if hr value is valid
        """


    @push_data('sp02')
    def add_sp02_data(self, uuid, date, time, sp02, sp02_valid):
        """
        Push SP02 data to database

        Args:
            uuid: Unique user idetification
            date: date of measurement ('%Y-%m-%d')
            time: time of measurement ('%H:%M:%S')
            sp02: sp02 value to push
            spo2_valid (bool): if sp02 value is valid
        """


    @push_data('jerk')
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


    @push_data('seat')
    def add_seat_data(self, uuid, date, time, seat):
        """
        Push seat load cell data to database

        Args:
            uuid: Unique user idetification
            date: date of measurement ('%Y-%m-%d')
            time: time of measurement ('%H:%M:%S')
            seat: seat load cell sensor values to push
        """


    @push_data('speed')
    def add_speed_data(self, uuid, date, time, speed):
        """
        Push speed data to database

        Args:
            uuid: Unique user idetification
            date: date of measurement ('%Y-%m-%d')
            time: time of measurement ('%H:%M:%S')
            seat: seat load cell sensor values to push
        """


    @push_data('weightDistribution')
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
