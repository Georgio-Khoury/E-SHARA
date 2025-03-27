import smbus
import time

# MPU6050 I2C address
MPU6050_ADDR = 0x68

# MPU6050 Registers
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43
GYRO_ZOUT_H = 0x47

# Sensitivity factors (LSB per unit in SI)
ACCEL_SENSITIVITY = 16384.0  # �2g
GYRO_SENSITIVITY = 131.0     # �250�/s

# Initialize I2C bus
bus = smbus.SMBus(1)

# Wake up the MPU6050 (set the sleep mode to 0)
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

# Function to read 16-bit values (high and low byte)
def read_word(reg):
    high = bus.read_byte_data(MPU6050_ADDR, reg)
    low = bus.read_byte_data(MPU6050_ADDR, reg + 1)
    value = (high << 8) + low
    # Convert to signed value if necessary
    if value >= 0x8000:
        value -= 65536
    return value

# Read accelerometer data
def read_accel_data():
    accel_x = read_word(ACCEL_XOUT_H)
    accel_y = read_word(ACCEL_XOUT_H + 2)
    accel_z = read_word(ACCEL_XOUT_H + 4)
    return accel_x, accel_y, accel_z

# Read gyroscope data
def read_gyro_data():
    gyro_x = read_word(GYRO_XOUT_H)
    gyro_y = read_word(GYRO_XOUT_H + 2)
    gyro_z = read_word(GYRO_ZOUT_H)
    return gyro_x, gyro_y, gyro_z

# Function to convert raw accelerometer data to m/s�
def convert_accel_to_m_s2(raw_value):
    return raw_value / ACCEL_SENSITIVITY * 9.81  # m/s�

# Function to convert raw gyroscope data to degrees per second (�/s)
def convert_gyro_to_dps(raw_value):
    return raw_value / GYRO_SENSITIVITY  # �/s

try:
    while True:
        # Read accelerometer and gyroscope values
        accel_x, accel_y, accel_z = read_accel_data()
        gyro_x, gyro_y, gyro_z = read_gyro_data()

        # Convert accelerometer values to m/s�
        accel_x_m_s2 = convert_accel_to_m_s2(accel_x)
        accel_y_m_s2 = convert_accel_to_m_s2(accel_y)
        accel_z_m_s2 = convert_accel_to_m_s2(accel_z)

        # Convert gyroscope values to �/s
        gyro_x_dps = convert_gyro_to_dps(gyro_x)
        gyro_y_dps = convert_gyro_to_dps(gyro_y)
        gyro_z_dps = convert_gyro_to_dps(gyro_z)

        # Print the values in SI units
        print(f"Accelerometer (m/s�): X={accel_x_m_s2:.2f}, Y={accel_y_m_s2:.2f}, Z={accel_z_m_s2:.2f}")
        print(f"Gyroscope (�/s): X={gyro_x_dps:.2f}, Y={gyro_y_dps:.2f}, Z={gyro_z_dps:.2f}")

        # Sleep before the next reading
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Exiting program.")


#this code reads the raw accelerometer and gyroscope data from the MPU6050 sensor, converts it to SI units (m/s� for acceleration and �/s for angular velocity), and prints the values to the console. The program runs in an infinite loop, reading the sensor values every 0.01 seconds. The program can be terminated by pressing Ctrl + C, which will print "Exiting program." to the console.