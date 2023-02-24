"""
Strain Gauge
"""
import smbus

class DaokiBF3503AA():
    def __init__(self, gpioA, address):
        self.gpioChannelA = gpioA
        self.address = address
        self.bus = smbus.SMBus(self.gpioChannelA)

    def get_raw_sensor_data(self):
        # read sensor data from pins
        return self.bus.read_byte(self.address)
    
    def get_processed_sensor_data(self):
         # process raw sensor data into something useful to read
        raw = self.get_raw_sensor_data()
        return raw*10