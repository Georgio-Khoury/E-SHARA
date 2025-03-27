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

def read_mcp3008(channel):
    """Reads analog value from MCP3008 ADC."""
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
        with lock:
            fsr1_value.value = read_mcp3008(7)
            fsr2_value.value = read_mcp3008(6)
            fsr3_value.value = read_mcp3008(5)
        time.sleep(0.1)
    print("FSR reader finished.")

def flex_reader(flex1_value, flex2_value, flex3_value, flex4_value, flex5_value, lock):
    """Reads flex sensor values continuously and stores them in shared memory."""
    print("Flex sensor reader started.")
    start_time = time.time()
    while time.time() - start_time < 8:
        with lock:
            flex1_value.value = read_mcp3008(0)
            flex2_value.value = read_mcp3008(1)
            flex3_value.value = read_mcp3008(2)
            flex4_value.value = read_mcp3008(3)
            flex5_value.value = read_mcp3008(4)
        time.sleep(0.1)
    print("Flex sensor reader finished.")

def imu_reader(fsr1_value, fsr2_value, fsr3_value, flex1_value, flex2_value, flex3_value, flex4_value, flex5_value, lock):
    """Reads IMU data and stores it along with FSR and Flex sensor values in a buffer."""
    print("IMU reader started. Collecting data...")
    data_buffer = []
    start_time = time.time()
    
    while time.time() - start_time < 10:
        accel_x, accel_y, accel_z = read_accel_data()
        gyro_x, gyro_y, gyro_z = read_gyro_data()

        accel_x_m_s2 = convert_accel_to_m_s2(accel_x)
        accel_y_m_s2 = convert_accel_to_m_s2(accel_y)
        accel_z_m_s2 = convert_accel_to_m_s2(accel_z)

        gyro_x_dps = convert_gyro_to_dps(gyro_x)
        gyro_y_dps = convert_gyro_to_dps(gyro_y)
        gyro_z_dps = convert_gyro_to_dps(gyro_z)

        with lock:
            data_buffer.append([time.time(), accel_x_m_s2, accel_y_m_s2, accel_z_m_s2,
                                gyro_x_dps, gyro_y_dps, gyro_z_dps, fsr1_value.value,
                                fsr2_value.value, fsr3_value.value, flex1_value.value,
                                flex2_value.value, flex3_value.value, flex4_value.value,
                                flex5_value.value])
    
    print("IMU data collection finished. Writing to CSV...")
    with open('imu_fsr_flex_dataset.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'accel_x_m_s2', 'accel_y_m_s2', 'accel_z_m_s2',
                         'gyro_x_dps', 'gyro_y_dps', 'gyro_z_dps', 'fsr1_value', 'fsr2_value', 'fsr3_value',
                         'flex1_value', 'flex2_value', 'flex3_value', 'flex4_value', 'flex5_value'])
        writer.writerows(data_buffer)
    
    print("Dataset writing complete.")

def main():
    """Main function to start multiprocessing data collection."""
    fsr1_value = Value('i', 0)
    fsr2_value = Value('i', 0)
    fsr3_value = Value('i', 0)
    flex1_value = Value('i', 0)
    flex2_value = Value('i', 0)
    flex3_value = Value('i', 0)
    flex4_value = Value('i', 0)
    flex5_value = Value('i', 0)
    lock = Lock()

    fsr_process = Process(target=fsr_reader, args=(fsr1_value, fsr2_value, fsr3_value, lock))
    flex_process = Process(target=flex_reader, args=(flex1_value, flex2_value, flex3_value, flex4_value, flex5_value, lock))
    imu_process = Process(target=imu_reader, args=(fsr1_value, fsr2_value, fsr3_value, flex1_value, flex2_value, flex3_value, flex4_value, flex5_value, lock))
    
    print("Starting data collection...")
    fsr_process.start()
    flex_process.start()
    imu_process.start()

    fsr_process.join()
    flex_process.join()
    imu_process.join()

    print("Dataset recording complete.")

if __name__ == '__main__':
    main()

