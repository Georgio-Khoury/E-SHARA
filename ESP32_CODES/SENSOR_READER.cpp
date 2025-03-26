#include <Wire.h>
#include <MPU6050_tockn.h>

MPU6050 mpu(Wire);

#define NUM_FLEX 5
#define NUM_FSR 3

// Define Analog Pins
const int flexPins[NUM_FLEX] = {32, 33, 34, 35, 36};
const int fsrPins[NUM_FSR] = {39, 25, 26};

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

    mpu.begin();
    mpu.calcGyroOffsets(true);
    
    Serial.println("MPU6050 + Flex + FSR initialized!");
}

void loop() {
    unsigned long startTime = millis();
    unsigned long duration = 10000; // 10 seconds
    unsigned long currentTime;
    
    while (millis() - startTime < duration) {
        SensorData data;
        currentTime = millis() / 1000;  // Get UNIX timestamp (seconds)
        data.timestamp = currentTime;

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

    // Print the collected data (Sensor Log)
    Serial.println("\nTimestamp | AccX | AccY | AccZ | GyroX | GyroY | GyroZ | Flex1 | Flex2 | Flex3 | Flex4 | Flex5 | FSR1 | FSR2 | FSR3");
    for (const auto& entry : sensorLog) {
        Serial.print(entry.timestamp); Serial.print(" | ");
        Serial.print(entry.accX); Serial.print(" | ");
        Serial.print(entry.accY); Serial.print(" | ");
        Serial.print(entry.accZ); Serial.print(" | ");
        Serial.print(entry.gyroX); Serial.print(" | ");
        Serial.print(entry.gyroY); Serial.print(" | ");
        Serial.print(entry.gyroZ); Serial.print(" | ");
        
        for (int i = 0; i < NUM_FLEX; i++) {
            Serial.print(entry.flex[i]); Serial.print(" | ");
        }

        for (int i = 0; i < NUM_FSR; i++) {
            Serial.print(entry.fsr[i]); Serial.print(" | ");
        }

        Serial.println();
    }

    // End the program (optional, loop will stop)
    while (true);
}
