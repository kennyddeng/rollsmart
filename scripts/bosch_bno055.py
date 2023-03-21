#!/usr/bin/env python3
# pylint: disable=invalid-name, logging-fstring-interpolation, broad-exception-caught
"""
Script to interface with Bosch BNO0555
"""
import board
import adafruit_bno055

last_val = 0xFFFF


class BoschBNO055():
    """
    Class to interface with BoschBNO055 IMU sensor

    requires adafruit-circuitpython-bno055 library
    """
    def __init__(self, logger):
        self.logger = logger

        try:
            self.i2c = board.I2C()
            self.imu_sensor = adafruit_bno055.BNO055_I2C(self.i2c)
            self.connected = True
            self.log_values(message="Connected!")
        except Exception as e:
            self.connected = False
            self.log_values(message="Unable to connect to sensor!")
            self.log_values(message=e)

    def temperature(self):
        """
        Process sensor temperature value
        """
        global last_val  # pylint: disable=global-statement
        result = self.imu_sensor.temperature
        if abs(result - last_val) == 128:
            result = self.imu_sensor.temperature
            if abs(result - last_val) == 128:
                return 0b00111111 & result
        last_val = result
        return result

    def get_processed_sensor_data(self):
        """
        process raw sensor data into something useful to read
        """
        if self.connected:
            temperature = self.temperature()
            acceleration = self.imu_sensor.acceleration
            magnetic = self.imu_sensor.magnetic
            gyro = self.imu_sensor.gyro
            euler = self.imu_sensor.euler
            quaternion = self.imu_sensor.quaternion
            gravity = self.imu_sensor.gravity
            linear_accel = self.imu_sensor.linear_acceleration
            imu_val = [temperature, acceleration, magnetic, gyro, euler,
                       quaternion, gravity,linear_accel]
        else:
            imu_val = None
        return imu_val

    def log_values(self, imu_val=None, message=None):
        """
        log processed sensor data
        """
        log_col = '[bold gold1]'
        value_col = '[orange1]'
        if message is not None:
            self.logger.warning(f'{log_col}IMU (BNO0555)[/]: {value_col}{message}[/]')
        elif imu_val is not None:
            self.logger.info(f"Temperature: {imu_val[0]} degrees C")
            self.logger.info(f"Accelerometer (m/s^2): {imu_val[1]}")
            self.logger.info(f"Magnetometer (microteslas): {imu_val[2]}")
            self.logger.info(f"Gyroscope (rad/sec): {imu_val[3]}")
            self.logger.info(f"Euler angle: {imu_val[4]}")
            self.logger.info(f"Quaternion: {imu_val[5]}")
            self.logger.info(f"Linear acceleration (m/s^2): {imu_val[6]}")
            self.logger.info(f"Gravity (m/s^2): {imu_val[7]}")
        else:
            self.logger.info(f'{log_col}IMU (BNO055)[/]: value={value_col}{imu_val}[/]')
