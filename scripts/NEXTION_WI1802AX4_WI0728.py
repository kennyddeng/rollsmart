"""
Load Cell
"""

class NEXTION_WI1802AX4_WI0728():
    def __init__(self):
        self._gpioChannelA = 0
        self._gpioChannelB = 1
        self._gpioChannelC = 2
    
    def _get_raw_sensor_data(self):
        # read sensor data from pins
        return 42
    
    def _process_raw_sensor_data(self):
        # process raw sensor data into something useful to read
        return 21

    def _write_data_to_database(self):
        write_to_db = 123