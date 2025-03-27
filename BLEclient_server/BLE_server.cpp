#include <ArduinoBLE.h>
#include <Arduino_LSM9DS1.h> 

#define NUM_COLUMNS 14  

BLEService sensorService("12345678-1234-5678-1234-56789abcdef0"); 
BLECharacteristic sensorCharacteristic("87654321-4321-6789-4321-6789abcdef01", BLERead | BLENotify, 64);

int fsrPins[3] = {A0, A1, A2};
int flexPins[5] = {A3, A4, A5, A6, A7};

void setup() {
    Serial.begin(115200);
    while (!Serial);

    if (!BLE.begin()) {
        Serial.println("Failed to initialize BLE!");
        while (1);
    }

    if (!IMU.begin()) {
        Serial.println("IMU initialization failed!");
        while (1);
    }

    BLE.setLocalName("BLE_Sensor_Server");
    BLE.setAdvertisedService(sensorService);
    sensorService.addCharacteristic(sensorCharacteristic);
    BLE.addService(sensorService);
    sensorCharacteristic.writeValue("Initializing...");

    BLE.advertise();
    Serial.println("BLE Sensor Server is running...");
}

void loop() {
    BLEDevice central = BLE.central();
    if (central) {
        Serial.print("Connected to: ");
        Serial.println(central.address());

        while (central.connected()) {
            String dataPacket = "";

            // Read FSR values
            for (int i = 0; i < 3; i++) {
                dataPacket += String(analogRead(fsrPins[i])) + ",";
            }

            // Read Flex sensor values
            for (int i = 0; i < 5; i++) {
                dataPacket += String(analogRead(flexPins[i])) + ",";
            }

            // Read IMU values (Acceleration + Rotation)
            float ax, ay, az, gx, gy, gz;
            if (IMU.accelerationAvailable() && IMU.gyroscopeAvailable()) {
                IMU.readAcceleration(ax, ay, az);
                IMU.readGyroscope(gx, gy, gz);
            }

            // Append IMU values
            dataPacket += String(ax, 2) + "," + String(ay, 2) + "," + String(az, 2) + ",";
            dataPacket += String(gx, 2) + "," + String(gy, 2) + "," + String(gz, 2);

            sensorCharacteristic.writeValue(dataPacket.c_str());
            Serial.println("Sent: " + dataPacket);

            delay(100); 
        }

        Serial.println("Disconnected");
    }
}
