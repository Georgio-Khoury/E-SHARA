#include <Wire.h>
#include <MPU6050_tockn.h>
#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <vector>

MPU6050 mpu(Wire);

// Define Sensor Constants
#define NUM_FLEX 5
#define NUM_FSR 3

// Define Analog Pins
const int flexPins[NUM_FLEX] = {32, 33, 34, 35, 36};
const int fsrPins[NUM_FSR] = {39, 25, 26};

// Bluetooth UUIDs
#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

BLECharacteristic *pCharacteristic;
bool deviceConnected = false;
bool startSignalReceived = false;  // Flag to track if the "START" signal is received

// Bluetooth Callbacks
class MyServerCallbacks : public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
        deviceConnected = true;
        Serial.println("Device Connected!");
    }

    void onDisconnect(BLEServer* pServer) {
        deviceConnected = false;
        Serial.println("Device Disconnected!");
        BLEDevice::startAdvertising();  // Restart advertising for reconnection
    }
};

class MyReceiveCallbacks : public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic* pCharacteristic) {
        // Convert the value from String to std::string
        std::string value = pCharacteristic->getValue().c_str();  // .c_str() converts String to const char*

        if (value == "START") {
            Serial.println("Received: START signal");
            startSignalReceived = true;  // Set the flag to start data collection
        }
        else if (value == "STOP") {
            Serial.println("Received: STOP signal");
            // Handle stop signal if necessary
        }
    }
};

// Data Structure
struct SensorData {
    unsigned long timestamp;  // Time in UNIX timestamp
    float accX, accY, accZ;
    float gyroX, gyroY, gyroZ;
    int flex[NUM_FLEX];
    int fsr[NUM_FSR];
};

// List to store sensor readings
std::vector<SensorData> sensorLog;

void setup() {
    Serial.begin(115200);
    Wire.begin();

    // Initialize MPU6050
    mpu.begin();
    mpu.calcGyroOffsets(true);
    Serial.println("MPU6050 Initialized!");

    // Initialize Bluetooth
    BLEDevice::init("ESP32_Sensor_BLE");
    BLEDevice::setMTU(512); // Increase MTU to allow larger messages

    BLEServer *pServer = BLEDevice::createServer();
    pServer->setCallbacks(new MyServerCallbacks());
    
    BLEService *pService = pServer->createService(SERVICE_UUID);
    pCharacteristic = pService->createCharacteristic(
        CHARACTERISTIC_UUID,
        BLECharacteristic::PROPERTY_READ |
        BLECharacteristic::PROPERTY_NOTIFY |
        BLECharacteristic::PROPERTY_WRITE
    );
    pCharacteristic->setCallbacks(new MyReceiveCallbacks());  // Set the callback for handling writes

    pService->start();
    BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(SERVICE_UUID);
    pAdvertising->setScanResponse(true);
    pAdvertising->setMinPreferred(0x06);
    pAdvertising->setMinPreferred(0x12);
    BLEDevice::startAdvertising();
    
    Serial.println("BLE Ready!");
}

void loop() {
    if (startSignalReceived) {
        unsigned long startTime = millis();
        unsigned long duration = 5000; // 10 seconds

        sensorLog.clear();  // Clear previous data
        unsigned long test = 1;
        
        // Collect data for 10 seconds
        while (millis() - startTime < duration) {
            SensorData data;
            data.timestamp = test;
            test++;
            
            // Read MPU6050
            mpu.update();
            data.accX = mpu.getAccX();
            data.accY = mpu.getAccY();
            data.accZ = mpu.getAccZ();
            data.gyroX = mpu.getGyroX();
            data.gyroY = mpu.getGyroY();
            data.gyroZ = mpu.getGyroZ();

            // Read Flex Sensors
            for (int i = 0; i < NUM_FLEX; i++) {
                data.flex[i] = analogRead(flexPins[i]);
            }

            // Read FSR Sensors
            for (int i = 0; i < NUM_FSR; i++) {
                data.fsr[i] = analogRead(fsrPins[i]);
            }

            // Store data in list
            sensorLog.push_back(data);

            delay(20);  // 50Hz sampling rate (20ms delay)
        }
        Serial.println("Sensor Reading Finished");
        // Send data over Bluetooth if connected and if there's data to send
        if (deviceConnected && !sensorLog.empty()) {
            Serial.println("Sending Data...");

            // Iterate over the collected data and send it
            for (size_t i = 0; i < sensorLog.size(); i++) {
                const auto& entry = sensorLog[i];
                String message = String(entry.timestamp) + "," +
                                 String(entry.accX) + "," + String(entry.accY) + "," + String(entry.accZ) + "," +
                                 String(entry.gyroX) + "," + String(entry.gyroY) + "," + String(entry.gyroZ);

                for (int i = 0; i < NUM_FLEX; i++) {
                    message += "," + String(entry.flex[i]);
                }

                for (int i = 0; i < NUM_FSR; i++) {
                    message += "," + String(entry.fsr[i]);
                }

                // Send the message to the connected BLE client
                pCharacteristic->setValue(message.c_str());
                pCharacteristic->notify();
                //Serial.println("Sent: " + message +" size: "+ message.length());
                delay(15);
               // sendLargeMessage(message);
                 
            }

             // Send "DONE" message and wait for ACK
            delay(20); 
            bool ackReceived = false;
            unsigned long ackStartTime = millis();
            int doneSent=0;
            while (!ackReceived&&doneSent<3) {
                String doneMessage = "DONE";
                pCharacteristic->setValue(doneMessage.c_str());
                pCharacteristic->notify();
                Serial.println("Sent: DONE");
                doneSent++;

                // Wait for ACK
                unsigned long timeout = 5000; // 3 seconds timeout for ACK
                while (millis() - ackStartTime < timeout) {
                  Serial.println(pCharacteristic->getValue());
                    if (pCharacteristic->getValue() == "ACK") { // Check for ACK
                        Serial.println("ACK received.");
                        ackReceived = true;
                        break;
                    }
                    delay(100);
                }

                if (!ackReceived&&doneSent<3) {
                    Serial.println("ACK not received, resending DONE...");
                    ackStartTime = millis(); // Reset timer for retry
                }else if(!ackReceived&&doneSent==3){
                  Serial.println("ACK not received, connection issue.");
                }
            }


            // Once all data is sent, clear the log to indicate completion
            sensorLog.clear();  // Data transmission complete, clear sensor log
            Serial.println("Data transmission complete.");
        } else {
            Serial.println("No data to send or BLE device not connected.");
        }

        // Reset startSignalReceived flag and wait for the next "START" signal
        startSignalReceived = false;
        Serial.println("Waiting for the next START signal...");
    }
}

void sendLargeMessage(String message) {
    int maxPacketSize = 20; // Adjust based on MTU (typically 512)
    int messageLength = message.length();
    int chunkCount = 0;

    for (int i = 0; i < messageLength; i += maxPacketSize) {
        String chunk = message.substring(i, i + maxPacketSize);
        pCharacteristic->setValue(chunk.c_str());
        pCharacteristic->notify();
        chunkCount++;
        Serial.println("Sent chunk " + String(chunkCount) + " of " + String((message.length() + maxPacketSize - 1) / maxPacketSize));
        delay(18);  // Delay to avoid packet loss
    }

    // After sending all chunks, send "ROW_END" to indicate the end of the row
    String rowEndMessage = "ROW_END";  // Special marker to signal end of row
    pCharacteristic->setValue(rowEndMessage.c_str());
    pCharacteristic->notify();
    Serial.println("Sent: ROW_END");
}
