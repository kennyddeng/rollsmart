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
        except Exception as e:
            print(e)

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
        return imu_val

    def log_values(self, imu_val):
        """
        log processed sensor data
        """
        self.logger.log(f"Temperature: {imu_val[0]} degrees C")
        self.logger.log(f"Accelerometer (m/s^2): {imu_val[1]}")
        self.logger.log(f"Magnetometer (microteslas): {imu_val[2]}")
        self.logger.log(f"Gyroscope (rad/sec): {imu_val[3]}")
        self.logger.log(f"Euler angle: {imu_val[4]}")
        self.logger.log(f"Quaternion: {imu_val[5]}")
        self.logger.log(f"Linear acceleration (m/s^2): {imu_val[6]}")
        self.logger.log(f"Gravity (m/s^2): {imu_val[7]}")
