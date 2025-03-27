from bluepy import btle

ESP32_MAC_ADDRESS = "fc:b4:67:f5:4b:ba"
SERVICE_UUID = "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
CHARACTERISTIC_UUID = "beb5483e-36e1-4688-b7f5-ea07361b26a8"

class MyDelegate(btle.DefaultDelegate):
    def __init__(self):
        btle.DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print("Received:", data.decode())

print("Connecting to ESP32...")
try:
    device = btle.Peripheral(ESP32_MAC_ADDRESS)
    device.setDelegate(MyDelegate())
    
    service = device.getServiceByUUID(SERVICE_UUID)
    characteristic = service.getCharacteristics(CHARACTERISTIC_UUID)[0]
    
    # Enable notifications
    characteristic.write(b"\x01\x00", withResponse=True)
    
    print("Connected! Waiting for notifications...")
    while True:
        if device.waitForNotifications(1.0):
            continue
except btle.BTLEException as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("Disconnecting...")
    device.disconnect()
