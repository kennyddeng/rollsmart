#!/usr/bin/env python
# pylint: disable=too-few-public-methods, invalid-name
"""
Nextion W1802AXWI0728 Module wrapper to simplify rollsmart operations
"""
from nextion_wi1802ax4_wi0728 import NextionWI1802AX4WI0728


class NextionLC():
    """
    Class to interface with Nextion Load Cell
    """
    def __init__(self, logger, load_cell_dout=23, load_cell_sck=24, load_cell_reference_value=100):
        self.logger = logger
        self.load_cell_dout = load_cell_dout
        self.load_cell_sck = load_cell_sck
        self.load_cell_reference_value = load_cell_reference_value

        try:
            self.load_cell = NextionWI1802AX4WI0728(self.load_cell_dout, self.load_cell_sck)

            # confgure load cell sensor``
            self.load_cell.set_reading_format("MSB", "MSB")
            self.load_cell.set_reference_unit(self.load_cell_reference_value)
            self.load_cell.reset()
            self.load_cell.tare()
            self.connected = True
            self.log_value(message='Connected!')
        except Exception:
            self.log_value(message='Unable to connect to sensor!')

    def get_processed_sensor_data(self):
        """
        Requests load cell value from sensors, and performs power cycle
        """
        load_cell_val = self.load_cell.get_weight(5)
        self.load_cell.power_down()
        self.load_cell.power_up()
        return load_cell_val

    def log_value(self, value=None, message=None):
        """
        Return Rich formatted logging message for load cell value
        """
        log_col = '[bold slate_blue1]'
        value_col = '[light_slate_blue]'
        if message is not None:
            self.logger.warning(f'{log_col}LOADCELL (Nextion)[/]: {value_col}{message}[/]')
        else:
            self.logger.info(f'{log_col}LOADCELL (Nextion)[/]: value={value_col}{value}[/]')
