"""
IMU

requires adfruit_bno055 library
pip3 install adafruit-circuitpython-bno055
"""

import time
import board
import adafruit_bno055


#i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
#sensor = adafruit_bno055.BNO055_I2C(i2c)

uart = board.UART()
sensor = adafruit_bno055.BNO055_UART(uart)

last_val = 0xFFFF





class BoschBNO055():
    def __init__(self, gpioA):
        self.gpioChannelA = gpioA
        self.i2c = board.I2C()
        self.imu_sensor = adafruit_bno055.BNO055_I2C(self.i2c)

    def temperature():
        global last_val  # pylint: disable=global-statement
        result = sensor.temperature
        if abs(result - last_val) == 128:
            result = sensor.temperature
            if abs(result - last_val) == 128:
                return 0b00111111 & result
        last_val = result
        return result

    def get_processed_sensor_data(self):
        # process raw sensor data into something useful to read
        temperature = self.temperature()
        acceleration = self.imu_sensor.acceleration
        magnetic = self.imu_sensor.magnetic
        gyro = self.imu_sensor.gyro
        euler = self.imu_sensor.euler
        quaternion = self.imu_sensor.quaternion
        gravity = self.imu_sensor.gravity
        linear_accel = self.imu_sensor.linear_acceleration

        return temperature, euler, gravity

    def prin_processed_sensor_data(self):
        # print processed sensor data
        while True:
            print("Temperature: {} degrees C".format(self.temperature())
            print("Accelerometer (m/s^2): {}".format(sensor.acceleration))
            print("Magnetometer (microteslas): {}".format(sensor.magnetic))
            print("Gyroscope (rad/sec): {}".format(sensor.gyro))
            print("Euler angle: {}".format(sensor.euler))
            print("Quaternion: {}".format(sensor.quaternion))
            print("Linear acceleration (m/s^2): {}".format(sensor.linear_acceleration))
            print("Gravity (m/s^2): {}".format(sensor.gravity))
            print()

            time.sleep(1)

