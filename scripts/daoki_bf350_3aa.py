# pylint: disable=import-error
"""
Strain Gauge
"""
try:
    import smbus
except:
    import smbus2 as smbus


class DaokiBF3503AA():
    """
    Class to interface with Daoki BF3503AA Strain gauge.

    These sensors are attached to the handles of the rollator to determine the users
    weigt distribution while using the device

    Args:
        gpio: Raspberry Pi GPIO pin
        address: i2c address for sensor
    """
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
