import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device (CE0)
spi.mode=0
spi.max_speed_hz = 1000000  # Set SPI speed (1 MHz)

# Function to read ADC value from MCP3008
def read_adc(channel):
    if channel < 0 or channel > 7:
        return -1  # Invalid channel

    # MCP3008 SPI protocol: 1 start bit, channel selection, and 1 null bit
    adc_data = spi.xfer2([1, (8 + channel) << 4, 0])
    adc_value = ((adc_data[1] & 3)) << 8 | adc_data[2]
    return adc_value

try:
    while True:
        # Read the flex sensor value from channel 7
        flex_value = read_adc(7)
        print(f"Flex Sensor Value: {flex_value}")

        # Wait for a short time before reading again
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Exiting program.")

finally:
    spi.close()  # Close the SPI connection



 #this code simply reads the value of the flex sensor connected to channel 7 of the MCP3008 ADC and prints it to the console. The program runs in an infinite loop, reading the sensor value every 0.5 seconds. The program can be terminated by pressing Ctrl + C, which will print "Exiting program." to the console and close the SPI connection.   