#!/usr/bin/env python
"""
RollSmart Database Interface
"""
import firebase
import dbconfig


class Database():
    """
    Class which initializes, pushes and manages Firebase operations for RollSmart
    """
    def __init__(self):
        """
        Initialize Remote and Local databases
        """
        # initialize Firebase cloud database
        self.firebase = pyrebase.initialize_app(dbconfig.config)
        self.db = self.firebase.database()

        # initialize SQLite Local backup database
        self.sqlite_conn = sqlite3.connect('/home/pi/Documents/rollsmart/scripts/localDB.db')
	    self.sqlite_cursor = sqlite_conn.cursor()


    def push_sensor_data(self, entry, uuid, datatype, date, time, val):
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


    def push_sqlite(self, sensor, value, time, date):
        """
        Push to sqlite local database
        """
        sqlite_cursor.execute("INSERT INTO sensor_data (sensor_name, value, timestamp, date) VALUES (?, ?, ?, ?)", data)
        sqlite_conn.commit()
        print(f"To SQLite-> senName: {senName}, val:{val}, date: {date}, time: {time}")


    def check_internet_connection(self):
    """
    Check internet connection status
    """
        internet_status = True
        try:
            requests.get('https://www.google.com')
        except:
            internet_status = False

        return internet_status


if __name__ == '__main__':
    Database()

