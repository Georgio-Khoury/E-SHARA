import time
import multiprocessing
import spidev  # For MCP3008 communication
from mpu6050 import mpu6050  # For IMU communication
import csv

# SPI setup for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# IMU setup
imu = mpu6050(0x68)

# Sampling rates
IMU_RATE = 200  # Hz
FLEX_FSR_RATE = 10  # Hz

# Duration per gesture
GESTURE_DURATION = 4  # seconds

# Data buffers (use multiprocessing.Manager for shared memory)
manager = multiprocessing.Manager()
final_dataset = manager.list()
prev_flex_fsr_values = manager.list([0] * 8)  # Shared list for Flex + FSR sensors

# MCP3008 reading function
def read_mcp3008(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    return ((adc[1] & 3) << 8) + adc[2]

# IMU sampling function
def sample_imu(final_dataset, prev_flex_fsr_values):
    start_time = time.time()
    imu_sample_interval = 1 / IMU_RATE

    while time.time() - start_time < GESTURE_DURATION:
        # Read IMU data
        accel = imu.get_accel_data()
        gyro = imu.get_gyro_data()
        imu_vector = [accel['x'], accel['y'], accel['z'], gyro['x'], gyro['y'], gyro['z']]

        # Concatenate with the previous Flex/FSR values
        combined_vector = imu_vector + list(prev_flex_fsr_values)
        final_dataset.append(combined_vector)

        time.sleep(imu_sample_interval)

# Flex and FSR sampling function
def sample_flex_fsr(prev_flex_fsr_values):
    start_time = time.time()
    flex_fsr_sample_interval = 1 / FLEX_FSR_RATE

    while time.time() - start_time < GESTURE_DURATION:
        # Read values from the MCP3008
        flex_values = [read_mcp3008(i) for i in range(5)]  # Flex sensors on channels 0-4
        fsr_values = [read_mcp3008(i) for i in range(5, 8)]  # FSR sensors on channels 5-7

        # Update the shared Flex/FSR values
        prev_flex_fsr_values[:] = flex_values + fsr_values

        time.sleep(flex_fsr_sample_interval)

# Main function
def collect_gesture_data():
    global final_dataset
    
    # Reset buffer
    final_dataset[:] = []
    
    # Create processes for sampling
    imu_process = multiprocessing.Process(target=sample_imu, args=(final_dataset, prev_flex_fsr_values))
    flex_fsr_process = multiprocessing.Process(target=sample_flex_fsr, args=(prev_flex_fsr_values,))

    # Start processes
    imu_process.start()
    flex_fsr_process.start()

    # Wait for processes to finish
    imu_process.join()
    flex_fsr_process.join()

    # Save to CSV
    with open('gesture_data.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['accel_x', 'accel_y', 'accel_z', 'gyro_x', 'gyro_y', 'gyro_z',
                         'flex1', 'flex2', 'flex3', 'flex4', 'flex5', 
                         'fsr1', 'fsr2', 'fsr3'])
        writer.writerows(final_dataset)

    print("Data collection complete. Saved to 'gesture_data.csv'.")

# Run data collection
if __name__ == "__main__":
    collect_gesture_data()
