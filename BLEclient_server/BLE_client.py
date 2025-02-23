from bluepy import btle
import pandas as pd
import time

SENSOR_SERVICE_UUID = "12345678-1234-5678-1234-56789abcdef0"
SENSOR_CHARACTERISTIC_UUID = "87654321-4321-6789-4321-6789abcdef01"
MAC_ADDRESS = "BLE MAC ADDRESS"  

columns = ["Timestamp", "FSR1", "FSR2", "FSR3", "Flex1", "Flex2", "Flex3", "Flex4", "Flex5",
           "AccX", "AccY", "AccZ", "RotX", "RotY", "RotZ"]
data = []

class BLEClient(btle.DefaultDelegate):
    def __init__(self, addr):
        btle.DefaultDelegate.__init__(self)
        self.device = btle.Peripheral(addr)
        self.device.setDelegate(self)

    def handleNotification(self, cHandle, data):
        decoded_data = data.decode("utf-8").strip()
        sensor_values = decoded_data.split(",")

        if len(sensor_values) == 14:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            row = [timestamp] + [float(v) for v in sensor_values]
            data.append(row)
            print(f"Received row {len(data)}: {row}")

        if len(data) >= 600:  # Stop after 600 rows
            df = pd.DataFrame(data, columns=columns)
            df.to_csv("sensor_data.csv", index=False)
            print("\n Data collection complete! Saved to sensor_data.csv")
            self.device.disconnect()
            exit()

    def startListening(self):
        service = self.device.getServiceByUUID(SENSOR_SERVICE_UUID)
        characteristic = service.getCharacteristics(SENSOR_CHARACTERISTIC_UUID)[0]

        print(" Listening for sensor data...\n")
        while True:
            if self.device.waitForNotifications(1.0):
                continue
            print("⚠️ No notification received...")

if __name__ == "__main__":
    client = BLEClient(MAC_ADDRESS)
    client.startListening()
