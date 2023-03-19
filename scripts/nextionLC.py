#!/usr/bin/env python
"""
Nextion W1802AXWI0728 Module wrapper to simplify rollsmart operations
"""
from nextion_wi1802ax4_wi0728 import NextionWI1802AX4WI0728


class NextionLC():
    """
    Class to interface with Nextion Load Cell
    """
    def __init__(self, load_cell_dout=23, load_cell_sck=24, load_cell_reference_value=100):
        self.load_cell_dout = load_cell_dout
        self.load_cell_sck = load_cell_sck
        self.load_cell_reference_value = load_cell_reference_value

        self.load_cell = NextionWI1802AX4WI0728(self.load_cell_dout, self.load_cell_sck)

        # confgure load cell sensor``
        self.load_cell.set_reading_format("MSB", "MSB")
        self.load_cell.set_reference_unit(self.load_cell_reference_value)
        self.load_cell.reset()
        self.load_cell.tare()

    def get_processed_sensor_data(self):
        """
        Requests load cell value from sensors, and performs power cycle
        """
        load_cell_val = self.load_cell.get_weight(5)
        self.load_cell.power_down()
        self.load_cell.power_up()
        return load_cell_val

if __name__ == '__main__':
    NextionLC()

