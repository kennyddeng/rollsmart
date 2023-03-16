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

class MaxRefDes117():
    #def __init__(self, gpioA):
    def __init__(self):
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
        while True:
            red, ir = self.hr.read_sequential()
            hr = hrcalc.calc_hr_and_spo2(ir[:100], red[:100])
        return hr
