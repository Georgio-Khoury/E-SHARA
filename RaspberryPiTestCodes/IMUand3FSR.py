import smbus
import time
import csv
from multiprocessing import Process, Value, Lock
import spidev

# MPU6050 I2C address
MPU6050_ADDR = 0x68

# MPU6050 Registers
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43
GYRO_ZOUT_H = 0x47

# Sensitivity factors (LSB per unit in SI)
ACCEL_SENSITIVITY = 16384.0  # ±2g
GYRO_SENSITIVITY = 131.0     # ±250°/s

# Initialize I2C bus
bus = smbus.SMBus(1)

# Wake up the MPU6050 (set the sleep mode to 0)
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

# Initialize SPI for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

def read_word(reg):
    """Reads a 16-bit value from the specified MPU6050 register."""
    high = bus.read_byte_data(MPU6050_ADDR, reg)
    low = bus.read_byte_data(MPU6050_ADDR, reg + 1)
    value = (high << 8) + low
    if value >= 0x8000:
        value -= 65536
    return value

def read_accel_data():
    """Reads accelerometer data from MPU6050."""
    return (
        read_word(ACCEL_XOUT_H),
        read_word(ACCEL_XOUT_H + 2),
        read_word(ACCEL_XOUT_H + 4)
    )

def read_gyro_data():
    """Reads gyroscope data from MPU6050."""
    return (
        read_word(GYRO_XOUT_H),
        read_word(GYRO_XOUT_H + 2),
        read_word(GYRO_ZOUT_H)
    )

def convert_accel_to_m_s2(raw_value):
    """Converts raw accelerometer data to m/s²."""
    return raw_value / ACCEL_SENSITIVITY * 9.81

def convert_gyro_to_dps(raw_value):
    """Converts raw gyroscope data to degrees per second."""
    return raw_value / GYRO_SENSITIVITY

def read_fsr(channel):
    """Reads FSR value from MCP3008 ADC."""
    if channel < 0 or channel > 7:
        raise ValueError("Channel must be between 0 and 7")

    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    value = ((adc[1] & 3) << 8) + adc[2]
    return value

def fsr_reader(fsr1_value, fsr2_value, fsr3_value, lock):
    """Reads FSR values continuously and stores them in shared memory."""
    print("FSR reader started.")
    start_time = time.time()
    while time.time() - start_time < 8:
        fsr1 = read_fsr(7)  # Channel 7
        fsr2 = read_fsr(6)  # Channel 6
        fsr3 = read_fsr(5)  # Channel 5

        with lock:
            fsr1_value.value = fsr1
            fsr2_value.value = fsr2
            fsr3_value.value = fsr3

        time.sleep(0.1)
    print("FSR reader finished.")

def imu_reader(fsr1_value, fsr2_value, fsr3_value, lock):
    """Reads IMU data and stores it along with FSR values in a buffer."""
    print("IMU reader started. Collecting data...")
    data_buffer = []
    start_time = time.time()
    
    while time.time() - start_time < 8:
        accel_x, accel_y, accel_z = read_accel_data()
        gyro_x, gyro_y, gyro_z = read_gyro_data()

        accel_x_m_s2 = convert_accel_to_m_s2(accel_x)
        accel_y_m_s2 = convert_accel_to_m_s2(accel_y)
        accel_z_m_s2 = convert_accel_to_m_s2(accel_z)

        gyro_x_dps = convert_gyro_to_dps(gyro_x)
        gyro_y_dps = convert_gyro_to_dps(gyro_y)
        gyro_z_dps = convert_gyro_to_dps(gyro_z)

        with lock:
            fsr1 = fsr1_value.value
            fsr2 = fsr2_value.value
            fsr3 = fsr3_value.value

        timestamp = time.time()
        data_buffer.append([timestamp, accel_x_m_s2, accel_y_m_s2, accel_z_m_s2,
                            gyro_x_dps, gyro_y_dps, gyro_z_dps, fsr1, fsr2, fsr3])
    
    print("IMU data collection finished. Writing to CSV...")
    with open('imu_fsr_dataset_withbuffer.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'accel_x_m_s2', 'accel_y_m_s2', 'accel_z_m_s2',
                         'gyro_x_dps', 'gyro_y_dps', 'gyro_z_dps', 'fsr1_value', 'fsr2_value', 'fsr3_value'])
        writer.writerows(data_buffer)
    
    print("Dataset writing complete.")

def main():
    """Main function to start multiprocessing data collection."""
    fsr1_value = Value('i', 0)
    fsr2_value = Value('i', 0)
    fsr3_value = Value('i', 0)
    lock = Lock()

    fsr_process = Process(target=fsr_reader, args=(fsr1_value, fsr2_value, fsr3_value, lock))
    imu_process = Process(target=imu_reader, args=(fsr1_value, fsr2_value, fsr3_value, lock))
    
    print("Starting data collection...")
    fsr_process.start()
    imu_process.start()

    fsr_process.join()
    imu_process.join()

    print("Dataset recording complete.")

if __name__ == '__main__':
    main()
