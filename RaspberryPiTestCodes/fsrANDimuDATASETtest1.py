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
ACCEL_SENSITIVITY = 16384.0  # �2g
GYRO_SENSITIVITY = 131.0     # �250�/s

# Initialize I2C bus
bus = smbus.SMBus(1)

# Wake up the MPU6050 (set the sleep mode to 0)
bus.write_byte_data(MPU6050_ADDR, PWR_MGMT_1, 0)

# Initialize SPI for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000


def read_word(reg):
    high = bus.read_byte_data(MPU6050_ADDR, reg)
    low = bus.read_byte_data(MPU6050_ADDR, reg + 1)
    value = (high << 8) + low
    if value >= 0x8000:
        value -= 65536
    return value

def read_accel_data():
    return (
        read_word(ACCEL_XOUT_H),
        read_word(ACCEL_XOUT_H + 2),
        read_word(ACCEL_XOUT_H + 4)
    )

def read_gyro_data():
    return (
        read_word(GYRO_XOUT_H),
        read_word(GYRO_XOUT_H + 2),
        read_word(GYRO_ZOUT_H)
    )

def convert_accel_to_m_s2(raw_value):
    return raw_value / ACCEL_SENSITIVITY * 9.81

def convert_gyro_to_dps(raw_value):
    return raw_value / GYRO_SENSITIVITY

def read_fsr(channel=7):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    value = ((adc[1] & 3) << 8) + adc[2]
    return value

def fsr_reader(fsr_value, lock):
    start_time = time.time()
    while time.time() - start_time < 8:
        fsr = read_fsr()
        with lock:
            fsr_value.value = fsr
        time.sleep(0.1)

def imu_reader(fsr_value, lock):
    with open('imu_fsr_dataset.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['timestamp', 'accel_x_m_s2', 'accel_y_m_s2', 'accel_z_m_s2',
                         'gyro_x_dps', 'gyro_y_dps', 'gyro_z_dps', 'fsr_value'])

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
                fsr = fsr_value.value

            timestamp = time.time()
            writer.writerow([timestamp, accel_x_m_s2, accel_y_m_s2, accel_z_m_s2,
                             gyro_x_dps, gyro_y_dps, gyro_z_dps, fsr])

            time.sleep(0.005)

def main():
    fsr_value = Value('i', 0)
    lock = Lock()

    fsr_process = Process(target=fsr_reader, args=(fsr_value, lock))
    imu_process = Process(target=imu_reader, args=(fsr_value, lock))
    print("start")
    fsr_process.start()
    imu_process.start()

    fsr_process.join()
    imu_process.join()

    print("Dataset recording complete.")

if __name__ == '__main__':
    main()

#this code reads the accelerometer and gyroscope data from the MPU6050 sensor and the FSR data from the MCP3008 ADC. The accelerometer and gyroscope data are converted to SI units (m/s� and �/s) and the FSR data is read from channel 7 of the ADC. The data is then saved to a CSV file with a timestamp for each sample. The program runs for 8 seconds, sampling the data at a rate of 200 Hz for the IMU and 10 Hz for the FSR sensor. The program uses multiprocessing to read the FSR data in a separate process to avoid blocking the IMU sampling process. The data is saved to a CSV file named "imu_fsr_dataset.csv" in the same directory as the script. The program can be terminated by pressing Ctrl + C, which will print "Dataset recording complete." to the console.