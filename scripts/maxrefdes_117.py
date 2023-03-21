#!/usr/bin/env python3
# pylint: disable=invalid-name, logging-fstring-interpolation, broad-exception-caught
"""
Maxrefdes117# Hear Rate and SP02 sensor script which interfaces with max30102.py
"""
import max30102
import hrcalc
from utils.init_logger import init_logger


class MaxRefDes117():
    """
    Heart Rate Sensor : MAXREFDES117

    VIN --> 3.3V
    SDA --> I2C_SDA1 (pin3; GPIO 2)
    SLC --> I2C_SCL1 (pin5; GPIO 3)
    INT --> (pin7; GPIO 4)
    GND --> GND (pin9)
    """
    def __init__(self, logger):
        self.logger = logger or init_logger()
        try:
            self.hr = max30102.MAX30102()
            self.connected = True
            self.log_value(message='Connected!')
        except Exception as e:
            self.connected = False
            self.log_value(message='Unable to connect to sensor')
            self.log_value(message=e)

    def get_raw_sensor_data(self):
        """
        read sensor data from pins
        """
        red, ir = self.hr.read_sequential()
        return red, ir

    def get_processed_sensor_data(self):
        """
        process raw sensor data into something useful to read
        """
        if self.connected:
            red, ir = self.hr.read_sequential()
            hr, hr_valid, sp02, sp02_valid = hrcalc.calc_hr_and_spo2(ir[:100], red[:100])
        else:
            hr, hr_valid, sp02, sp02_valid = False, False, False, False
        return hr, hr_valid, sp02, sp02_valid

    def log_value(self, hr_val=None, sp02_val=None, message=None):
        """
        Return Rich formatted logging message for load cell value
        """
        log_col = '[bold deep_pink1]'
        value_col = '[deep_pink3]'
        if message is not None:
            self.logger.warning(f'{log_col}HR (MaxRefDes11)[/]: {value_col}{message}[/]')
        else:
            self.logger.info(f'{log_col}HR (MaxRefDes117)[/]: value={value_col}{hr_val}[/]')
            self.logger.info(f'{log_col}SP02 (MaxRefDes117)[/]: value={value_col}{sp02_val}[/]')
