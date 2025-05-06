from bluepy import btle
import time
import smbus
import spidev
import random
import csv
from multiprocessing import Process, Value, Lock, Event
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import matplotlib.pyplot as plt

READING_TIME = 10  # time to read each gest. in secs
# Bluetooth configuration
ESP32_MAC_ADDRESS = "fc:b4:67:f5:4b:ba"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

# MPU6050 I2C address and registers
MPU6050_ADDR = 0x68
PWR_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43
GYRO_ZOUT_H = 0x47
ACCEL_SENSITIVITY = 16384.0  # Â±2g
GYRO_SENSITIVITY = 131.0  # Â±250Â°/s

# Initialize I2C bus
bus = smbus.SMBus(1)

# Initialize SPI for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000


class MyDelegate(btle.DefaultDelegate):
    def __init__(self, characteristic, stop_event):
        btle.DefaultDelegate.__init__(self)
        self.characteristic = characteristic
        self.data = []
        self.stop_event = stop_event
        self.saved = False

    def handleNotification(self, cHandle, data):
        # print(f"Raw data received: {data}")  # Debugging
        decoded_data = data.decode()
        if decoded_data == "DONE":

            print("Received: DONE signal from ESP32")

            self.characteristic.write(
                b"ACK", withResponse=True
            )  # Now `characteristic` exists
            print("Sent: ACK to ESP32")
            if not self.saved:

                self.save_data_to_csv()
                self.saved = True
            self.stop_event.set()
            return
        self.data.append(decoded_data.split(","))

    def save_data_to_csv(self):
        print("entered save data")
        print(self.data)
        file_name = "data.csv"

        # Read existing data
        with open(file_name, mode="r", newline="") as file:
            reader = list(csv.reader(file))

        # Insert Bluetooth data into existing rows (starting from row 1, skipping the header)
        for i in range(
            1, min(len(reader), len(self.data) + 1)
        ):  # Ensure we don't exceed available rows
            reader[i].extend(
                self.data[i - 1]
            )  # Append Bluetooth data to existing IMU rows

        # Write updated data back to the file
        with open(file_name, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(reader)

        print("Bluetooth data merged into sensor_data.csv")


def connect(stop_event, start_event):
    while not stop_event.is_set():
        try:
            print("Connecting to ESP32...")
            device = btle.Peripheral(ESP32_MAC_ADDRESS)
            service = device.getServiceByUUID(SERVICE_UUID)
            characteristic = service.getCharacteristics(CHARACTERISTIC_UUID)[0]
            device.setMTU(100)  # Set MTU to 100

            delegate = MyDelegate(characteristic, stop_event)  # Pass the characteristic
            device.setDelegate(delegate)

            # Enable notifications
            characteristic.write(b"\x01\x00", withResponse=True)

            print("Connected! Sending START signal to ESP32...")
            characteristic.write(b"START", withResponse=True)
            start_event.set()
            print("Waiting for notifications...")
            while True:
                if device.waitForNotifications(1.0):
                    continue
                if stop_event.is_set():
                    break
        except btle.BTLEException as e:
            print(f"Connection lost: {e}. Reconnecting in 1 second...")
            time.sleep(1)
        except KeyboardInterrupt:
            print("Exiting...")
            break

def send_email(subject, body, attachment_path):
    sender_email = "aya.jouni02@lau.edu"
    receiver_emails = [
        "razan.hmede@lau.edu",
        "farah.alnassar@lau.edu",
        "georgio.elkhoury@lau.edu",
    ]
    sender_password = "your_password"  # Replace with your actual password

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ", ".join(receiver_emails)
    msg["Subject"] = subject

    
    msg.attach(MIMEText(body, "plain"))

 
    with open(attachment_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={attachment_path}")
        msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.office365.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_emails, msg.as_string())
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


def read_word(reg):
    """Reads a 16-bit value from the specified MPU6050 register."""
    # high = bus.read_byte_data(MPU6050_ADDR, reg)
    # low = bus.read_byte_data(MPU6050_ADDR, reg + 1)
    # value = (high << 8) + low
    # if value >= 0x8000:
    #   value -= 65536
    # return value
    return random.randint(-32768, 32768)


def read_accel_data():
    """Reads accelerometer data from MPU6050."""
    return (
        read_word(ACCEL_XOUT_H),
        read_word(ACCEL_XOUT_H + 2),
        read_word(ACCEL_XOUT_H + 4),
    )


def read_gyro_data():
    """Reads gyroscope data from MPU6050."""
    return (read_word(GYRO_XOUT_H), read_word(GYRO_XOUT_H + 2), read_word(GYRO_ZOUT_H))


def convert_accel_to_m_s2(raw_value):
    """Converts raw accelerometer data to m/sÂ²."""
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


def fsr_reader(fsr1_value, fsr2_value, fsr3_value, lock, start_event):
    """Reads FSR values continuously and stores them in shared memory."""
    start_event.wait()
    print("FSR reader started.")
    start_time = time.time()
    while time.time() - start_time < READING_TIME:
        with lock:
            fsr1_value.value = read_mcp3008(7)
            fsr2_value.value = read_mcp3008(6)
            fsr3_value.value = read_mcp3008(5)
        time.sleep(0.1)
    print("FSR reader finished.")


def flex_reader(
    flex1_value, flex2_value, flex3_value, flex4_value, flex5_value, lock, start_event
):
    """Reads flex sensor values continuously and stores them in shared memory."""
    start_event.wait()
    print("Flex sensor reader started.")
    start_time = time.time()
    while time.time() - start_time < READING_TIME:
        with lock:
            flex1_value.value = read_mcp3008(0)
            flex2_value.value = read_mcp3008(1)
            flex3_value.value = read_mcp3008(2)
            flex4_value.value = read_mcp3008(3)
            flex5_value.value = read_mcp3008(4)
        time.sleep(0.1)
    print("Flex sensor reader finished.")


def imu_reader(
    fsr1_value,
    fsr2_value,
    fsr3_value,
    flex1_value,
    flex2_value,
    flex3_value,
    flex4_value,
    flex5_value,
    lock,
    start_event,
):
    """Reads IMU data and stores it along with FSR and Flex sensor values in a buffer."""
    start_event.wait()
    print("IMU reader started. Collecting data...")
    data_buffer = []
    sampling_interval = 1 / 50  # 50hz
    start_time = time.time()
    index = 1

    while time.time() - start_time < READING_TIME:
        accel_x, accel_y, accel_z = read_accel_data()
        gyro_x, gyro_y, gyro_z = read_gyro_data()

        accel_x_m_s2 = convert_accel_to_m_s2(accel_x)
        accel_y_m_s2 = convert_accel_to_m_s2(accel_y)
        accel_z_m_s2 = convert_accel_to_m_s2(accel_z)

        gyro_x_dps = convert_gyro_to_dps(gyro_x)
        gyro_y_dps = convert_gyro_to_dps(gyro_y)
        gyro_z_dps = convert_gyro_to_dps(gyro_z)

        with lock:
            # Combine sensor data from the IMU and the FSR/Flex sensors
            data = [
                index,
                accel_x_m_s2,
                accel_y_m_s2,
                accel_z_m_s2,
                gyro_x_dps,
                gyro_y_dps,
                gyro_z_dps,
                fsr1_value.value,
                fsr2_value.value,
                fsr3_value.value,
                flex1_value.value,
                flex2_value.value,
                flex3_value.value,
                flex4_value.value,
                flex5_value.value,
            ]
            index = index + 1

            data_buffer.append(data)
        time.sleep(sampling_interval)  # Ensure 50 Hz sampling rate

    print("IMU data collection finished. Writing to CSV...")
    with open("data.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "index",
                "accel_x_m_s2",
                "accel_y_m_s2",
                "accel_z_m_s2",
                "gyro_x_dps",
                "gyro_y_dps",
                "gyro_z_dps",
                "fsr1_value",
                "fsr2_value",
                "fsr3_value",
                "flex1_value",
                "flex2_value",
                "flex3_value",
                "flex4_value",
                "flex5_value",
                "btindex",
                "BT_AccX",
                "BT_AccY",
                "BT_AccZ",
                "BT_GyroX",
                "BT_GyroY",
                "BT_GyroZ",
                "BT_Flex1",
                "BT_Flex2",
                "BT_Flex3",
                "BT_Flex4",
                "BT_Flex5",
                "BT_FSR1",
                "BT_FSR2",
                "BT_FSR3",
            ]
        )
        writer.writerows(data_buffer + [""] * 5)

    print("Dataset writing complete.")


def main():
    """Main function to start multiprocessing data collection."""
    fsr1_value = Value("i", 0)
    fsr2_value = Value("i", 0)
    fsr3_value = Value("i", 0)
    flex1_value = Value("i", 0)
    flex2_value = Value("i", 0)
    flex3_value = Value("i", 0)
    flex4_value = Value("i", 0)
    flex5_value = Value("i", 0)
    lock = Lock()
    start_event = Event()
    stop_event = Event()

    # Initialize Bluetooth delegate
    # delegate = MyDelegate(characteristic=None)

    # Start Bluetooth connection in a separate process
    bt_process = Process(target=connect, args=(stop_event, start_event))
    bt_process.start()

    # Start sensor reading processes
    fsr_process = Process(
        target=fsr_reader, args=(fsr1_value, fsr2_value, fsr3_value, lock, start_event)
    )
    flex_process = Process(
        target=flex_reader,
        args=(
            flex1_value,
            flex2_value,
            flex3_value,
            flex4_value,
            flex5_value,
            lock,
            start_event,
        ),
    )
    imu_process = Process(
        target=imu_reader,
        args=(
            fsr1_value,
            fsr2_value,
            fsr3_value,
            flex1_value,
            flex2_value,
            flex3_value,
            flex4_value,
            flex5_value,
            lock,
            start_event,
        ),
    )

    print("Starting data collection...")
    fsr_process.start()
    flex_process.start()
    imu_process.start()

    fsr_process.join()
    flex_process.join()
    imu_process.join()
    bt_process.join()

    subject = "Sensor Data from Raspberry Pi"
    body = "Attached is the latest sensor data collected from the Raspberry Pi."
    send_email(subject, body, "data.csv")
    print("Dataset recording complete.")

    # Plot the collected sensor data
    df = pd.read_csv('data.csv')

    sensor_columns = [
        'BT_AccX', 'BT_AccY', 'BT_AccZ',
        'BT_GyroX', 'BT_GyroY', 'BT_GyroZ',
        'BT_Flex1', 'BT_Flex2', 'BT_Flex3', 'BT_Flex4', 'BT_Flex5',
        'BT_FSR1', 'BT_FSR2', 'BT_FSR3'
    ]

    sensor_data = df[sensor_columns].apply(pd.to_numeric, errors='coerce')

    sensor_data.plot(subplots=True, figsize=(12, 10))
    plt.suptitle('Sensor Data After Header', fontsize=16)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
