//use the doit esp 32 devkit in the board selector on arduino ide

#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>

#define SERVICE_UUID        "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define CHARACTERISTIC_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"

BLECharacteristic *pCharacteristic;
BLEServer *pServer;
bool deviceConnected = false;

// Callback to handle disconnections
class MyServerCallbacks : public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) {
        deviceConnected = true;
        Serial.println("Device connected");
    }

    void onDisconnect(BLEServer* pServer) {
        deviceConnected = false;
        Serial.println("Device disconnected, restarting advertising...");
        BLEDevice::startAdvertising();  // Restart advertising when disconnected
    }
};

void setup() {
    Serial.begin(115200);
    Serial.println("Starting BLE...");

    BLEDevice::init("ESP32_BLE_HelloWorld");
    pServer = BLEDevice::createServer();
    pServer->setCallbacks(new MyServerCallbacks());  // Set the disconnect callback

    BLEService *pService = pServer->createService(SERVICE_UUID);

    pCharacteristic = pService->createCharacteristic(
        CHARACTERISTIC_UUID,
        BLECharacteristic::PROPERTY_READ |
        BLECharacteristic::PROPERTY_NOTIFY
    );

    pService->start();
    BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(SERVICE_UUID);
    pAdvertising->setScanResponse(true);
    pAdvertising->setMinPreferred(0x06);
    pAdvertising->setMinPreferred(0x12);
    BLEDevice::startAdvertising();

    Serial.println("BLE Ready and advertising!");
}

void loop() {
    if (deviceConnected) {
        String message = "Hello, World!";
        pCharacteristic->setValue(message.c_str());
        pCharacteristic->notify();
        Serial.println("Sent: " + message);
    }
    delay(1000);
}
