#!/usr/bin/env python
"""
Test upload
"""
import hrcalc
import logging
from rich import print
from rich.logging import RichHandler
from datetime import datetime as dt
from datetime import timedelta as td
#from maxrefdes_117 import MaxRefDes117
from database import Database

UID = "4nIlD4s8Jdc2Uoa1q0DeONmmisH2"


def main():
    """
    Send HR data to Firebase
    """
    # maxrefdes = MaxRefDes117()

    FORMAT = "%(message)s"
    logging.basicConfig(
        level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    logger = logging.getLogger('Rollsmart')

    print('im in main')
    while True:
        db = Database(logger)
        time_start = dt.today()
        date = dt.today().strftime('%Y-%m-%d')
        time_o = time_start + td(seconds=10)
        time = time_o.strftime('%H:%M:%S')
        hr, hr_valid, sp02, sp02_valid = get_sensor_data()
        print(f' test {hr}:{hr_valid}')
        db.add_hr_data(UID, date, time, hr)
        print(f'pushed {hr}:{hr_valid}')

def get_sensor_data():
    #get sensor data from test file
    time_start = dt.today()
    UID = "4nIlD4s8Jdc2Uoa1q0DeONmmisH2"
    with open("hr_log.txt", "r+") as f:
        date = dt.today().strftime('%Y-%m-%d')
        time = time_start.strftime('%H:%M:%S')
        first_line = f.readline()  # Read the first line of the file
        rest_of_lines = f.readlines()  # Read the rest of the lines in the file

        f.seek(0)  # Move the file pointer to the beginning of the file
        f.truncate()  # Clear the file

        f.write(''.join(rest_of_lines))  # Write the rest of the lines to the file
        f.write(first_line)
        red, ir, hr, hr_valid, sp02, sp02_valid = first_line.split(',')
        #addHRData(UID, date, time, hr)
    return hr, hr_valid, sp02, sp02_valid
if __name__ == '__main__':
    main()


