#!/usr/bin/env python
# pylint: disable=invalid-name, logging-fstring-interpolation
"""
Test  HR data upload
"""
import re
import fire
import logging
from datetime import datetime as dt
from datetime import timedelta as td
from rich.logging import RichHandler
#from maxrefdes_117 import MaxRefDes117
from database import Database


UID = "4nIlD4s8Jdc2Uoa1q0DeONmmisH2"
FORMAT = "%(message)s"

def main():
    """
    Send HR data to Firebase
    """
    # maxrefdes = MaxRefDes117()

    logging.basicConfig(
        level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    logger = logging.getLogger('Rollsmart')

    logger.info('Initializing HR Test main()')
    time_start = dt.today()
    while True:
        db = Database(logger)
        date = dt.today().strftime('%Y-%m-%d')
        time_o = time_start + td(seconds=10)
        time = time_o
        hr, hr_valid, sp02, sp02_valid = get_sensor_data()
        logger.info(f'HR = {hr}:{hr_valid}; SP02 = {sp02}:{sp02_valid}')
        db.add_hr_data(UID,time, hr, hr_valid)
        db.add_sp02_data(UID,time, sp02, sp02_valid)
        time_start = time_o

def get_sensor_data():
    """
    Test uploading HR sensor test data from hr_log.txt

    Verifies the database connection script
    """
    with open("hr_log.txt", "r+t", encoding='UTF-8') as file:
        first_line = file.readline()  # Read the first line of the file
        rest_of_lines = file.readlines()  # Read the rest of the lines in the file

        file.seek(0)  # Move the file pointer to the beginning of the file
        file.truncate()  # Clear the file

        file.write(''.join(rest_of_lines))  # Write the rest of the lines to the file
        file.write(first_line)
        _, _, hr, hr_valid, sp02, sp02_valid = first_line.split(',')
        pattern = r'(?<==)\d+'

        match = re.search(pattern, hr)
        if match:
            hr = match.group()
            print(hr)
        match_sp02 = re.search(pattern, sp02)
        if match_sp02:
            sp02 = match.group()
            print(sp02)
    return hr, hr_valid, sp02, sp02_valid


if __name__ == '__main__':
    main()
