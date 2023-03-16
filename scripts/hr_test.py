#!/usr/bin/env python
"""
Test upload
"""
import max30102
import hrcalc

from datetime import datetime as dt
from datetime import timedelta as td
from FBdataAdding import *
from maxrefdes_117 import MaxRefDes117

UID = "4nIlD4s8Jdc2Uoa1q0DeONmmisH2"


def main():
    """
    Send HR data to Firebase
    """
    maxrefdes = MaxRefDes117()
    print('im in main')
    while True:
        time_start = dt.today()
        date = dt.today().strftime('%Y-%m-%d')
        time_o = time_start + td(seconds=10)
        time = time_o.strftime('%H:%M:%S')
        hr, hr_valid, sp02, sp02_valid = maxrefdes.get_processed_sensor_data()
        print(f' test {hr}:{hr_valid}')
        addHRData(UID, date, time, hr)
        print(f'pushed {hr}:{hr_valid}')

if __name__ == '__main__':
    main()


