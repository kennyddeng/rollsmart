#!/usr/bin/env python
"""
Test upload
"""
import max30102
import hrcalc

from datetime import datetime as dt
from datetime import timedelta as td
from FBdataAdding import *
from maxrefdes_117 import get_processed_sensor_data

UID = "4nIlD4s8Jdc2Uoa1q0DeONmmisH2"


def main():
    """
    Send HR data to Firebase
    """
    time_start = dt.today()
    with open("hr_log.txt", "r") as f:
        for line in f:
            date = dt.today().strftime('%Y-%m-%d')
            time_o = time_start + td(seconds=10)
            time = time_o.strftime('%H:%M:%S')
            hr, hr_valid, sp02, sp02_valid = get_processed_sensor_data()
            addHRData(UID, date, time, hr)
            time_start = time_o

if __name__ == '__main__':
    main()


