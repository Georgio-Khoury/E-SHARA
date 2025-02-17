import smbus
import time

# MPU6050 I2C address
MPU6050_ADDR = 0x68

# MPU6050 Registers
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43

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
    gyro_z = read_word(GYRO_XOUT_H + 4)
    return gyro_x, gyro_y, gyro_z

try:
    while True:
        # Read accelerometer and gyroscope values
        accel_x, accel_y, accel_z = read_accel_data()
        gyro_x, gyro_y, gyro_z = read_gyro_data()

        # Print the values
        #print(f"Accelerometer: X={accel_x}, Y={accel_y}, Z={accel_z}")
        print(f"Gyroscope: X={gyro_x}, Y={gyro_y}, Z={gyro_z}")
        
        # Sleep before the next reading
        time.sleep(0.01)

except KeyboardInterrupt:
    print("Exiting program.")
