"""
IMU
"""

class BoschBNO055():
    def __init__(self):
        self.gpioChannelA = 1

    def get_raw_sensor_data(self):
        # read sensor data from pins
        return 42
    
    def get_processed_sensor_data(self):
         # process raw sensor data into something useful to read
        raw = self.get_raw_sensor_data()
        return raw*10