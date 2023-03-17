"""
Heart Rate Sensor : MAXREFDES117

VIN --> 3.3V
SDA --> I2C_SDA1 (pin3; GPIO 2)
SLC --> I2C_SCL1 (pin5; GPIO 3)
INT --> (pin7; GPIO 4)
GND --> GND (pin9)

"""
import max30102
import hrcalc
from datetime import datetime as dt
from datetime import timedelta as td
from FBdataAdding import *


class MaxRefDes117():
    #def __init__(self, gpioA):
    def __init__(self):
        print('Im innit')
        #self.gpioChannelA = gpioA
        try:
            self.hr = max30102.MAX30102()
        except Exception as e:
            print(e)


    def get_raw_sensor_data(self):
        # read sensor data from pins
        red, ir = self.hr.read_sequential()
        return red, ir

    def get_processed_sensor_data(self):
         # process raw sensor data into something useful to read
        red, ir = self.hr.read_sequential()
        hr, hr_valid, sp02, sp02_valid = hrcalc.calc_hr_and_spo2(ir[:100], red[:100])
        print(f'{hr}:{hr_valid}, {sp02}:{sp02_valid}')
        return hr, hr_valid, sp02, sp02_valid

    def get_sensor_data(self):
        #get sensor data from test file
        time_start = dt.today()
        with open("hr_log.txt", "r+") as f:
            for line in f:
                date = dt.today().strftime('%Y-%m-%d')
                time = time_start.strftime('%H:%M:%S')
                first_line = f.readline()  # Read the first line of the file
                rest_of_lines = f.readlines()  # Read the rest of the lines in the file

                f.seek(0)  # Move the file pointer to the beginning of the file
                f.truncate()  # Clear the file

                f.write(''.join(rest_of_lines))  # Write the rest of the lines to the file
                f.write(first_line)
                red, ir, hr, hr_valid, sp02, sp02_valid = first_line.split(',')
                addHRData(UID, date, time, hr)

if __name__ == '__main__':
    MaxRefDes117()
