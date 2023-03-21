# pylint: disable=import-error, bare-except, broad-exception-caught
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
    def __init__(self, i2c_bus, gpio, address, logger):
        self.gpio_channel_a = gpio
        self.i2c_bus = i2c_bus
        self.address = address
        self.logger = logger
        try:
            self.get_raw_sensor_data()
            self.connected = True
            self.log_value(message='Connected!')
        except Exception as error:
            self.connected = False
            self.log_value(message='Unable to connect to Sensor!')
            self.log_value(message=error)

    def get_raw_sensor_data(self):
        """
        read sensor data from pins
        """
        return self.i2c_bus.read_byte(self.address)

    def get_processed_sensor_data(self):
        """
        process raw sensor data into something useful to read
        """
        if self.connected:
            raw = 10*(self.get_raw_sensor_data())
        else:
            raw = None
        return raw

    def log_value(self, side=None, value=None, message=None):
        """
        Return Rich formatted logging message for Strain gauge
        """
        log_col = '[bold spring_green3]'
        value_col = '[green]'
        if message is not None:
            self.logger.warning(f'{log_col}STRAIN {side} (Daoki)[/]: {value_col}{message}[/]')
        if side is not None:
            self.logger.info(f'{log_col}STRAIN {side} (Daoki)[/]: value={value_col}{value}[/]')
