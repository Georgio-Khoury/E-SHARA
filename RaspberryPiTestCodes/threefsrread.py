import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, device 0
spi.max_speed_hz = 1350000  # SPI clock speed

def read_mcp3008(channel):
    """Reads data from a specific MCP3008 channel (0-7)."""
    if channel < 0 or channel > 7:
        raise ValueError("Channel must be between 0 and 7")

    adc = spi.xfer2([1, (8 + channel) << 4, 0])  
    value = ((adc[1] & 3) << 8) + adc[2]  # Convert raw data
    return value

try:
    print("Reading MCP3008 channels 7 and 6. Press Ctrl+C to stop.")

    while True:
        value_ch7 = read_mcp3008(7)
        value_ch6 = read_mcp3008(6)
        value_ch5 = read_mcp3008(5)

        print(f"Channel 7: {value_ch7}, Channel 6: {value_ch6}, Channel 5: {value_ch5}")

        time.sleep(0.1)  # Adjust sampling rate if needed

except KeyboardInterrupt:
    print("\nStopped by user.")
    spi.close()
