# BLE Sensor Data Transmission--Arduino client to Raspberry Pi server

This project transmits sensor data from an **Arduino BLE microcontroller** to a **Raspberry Pi** over Bluetooth Low Energy (BLE). The data consists of:
- **3 FSR 402 sensors**
- **5 Flex sensors**
- **IMU (Acceleration: x, y, z & Rotation: x, y, z)**
- Data is logged in a CSV file on the Raspberry Pi with timestamps.

---

## Hardware Requirements

Connect the sensors to the Arduino BLE microcontroller 

##  Software Setup

### 🔹 1. Update Raspberry Pi

```bash
sudo apt update && sudo apt upgrade -y
```

### 🔹 2. Install the required packages

```bash
sudo apt install bluetooth bluez bluez-tools -y
pip install bluepy pandas
```

### 🔹 3. Upload BLE Server Code to Arduino

- **Be sure to connect the BLE Arduino to your laptop via USB**
- **Open Arduino IDE on your Laptop**
- **Install ArduinoBLE and Arduino_LSM9DS1 libraries**
- **Upload the BLE_server.cpp code to the arduino**
  
### 🔹 4. Verify BLE connection

Run the following commands on the Raspberry pi:

```bash
bluetoothctl

```

```bash
scan on
```

Find the Arduino BLE and note the MAC address to use it in the BLE_client.py code.

```bash
scan off
exit
```
  
### 🔹 5. Run the BLE_client.py file on the Raspberry pi

```bash
python3 BLE_client.py
```

### 🔹 6. Verify the sensor data collection

```bash
cat sensor_data.csv
```
