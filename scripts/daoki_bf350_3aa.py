"""
Strain Gauge
"""
import smbus

class DaokiBF3503AA():
    def __init__(self, gpio, address):
        self.gpio_channel_a = gpio
        self.address = address
        self.bus = smbus.SMBus(self.gpio_channel_a)

    def get_raw_sensor_data(self):
        """
        read sensor data from pins
        """
        return self.bus.read_byte(self.address)

    def get_processed_sensor_data(self):
        """
        process raw sensor data into something useful to read
        """
        raw = self.get_raw_sensor_data()
        return raw*10
