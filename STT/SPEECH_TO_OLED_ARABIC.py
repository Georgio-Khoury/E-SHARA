#Arabic speech to oled:
import time
import queue
import sys
import sounddevice as sd
import vosk
import json
from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from luma.core.render import canvas
from PIL import ImageFont  # Import ImageFont for text size calculation

# OLED Display Setup
def get_device():
    serial = i2c(port=1, address=0x3C)  # Adjust the address based on your OLED display
    return sh1106(serial)

# Speech Recognition Setup
MODEL_PATH = r"/home/pi/Downloads/vosk-model-ar-mgb2-0.4"  # Use Arabic model
SAMPLE_RATE = 16000

# Load Vosk model
model = vosk.Model(MODEL_PATH)

# Create a queue to store audio data
q = queue.Queue()

# Callback function to capture audio
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# Initialize recognizer
recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)

# Load Arabic font
def load_arabic_font():
    font_path = "/home/pi/Downloads/Rubik-VariableFont_wght.ttf"  # Replace with path to an Arabic font
    return ImageFont.truetype(font_path, size=14)  # Adjust size as needed

# Function to display Arabic text with line wrapping
def display_arabic_text(device, text, font):
    with canvas(device) as draw:
        y_position = 10  # Starting Y position
        line_height = 16  # Height of each line (adjust for Arabic font)
        max_width = device.width - 20  # Maximum width for text (with padding)
        words = text.split(" ")
        current_line = ""

        # Reverse the order of words for RTL text
        words = words[::-1]

        for word in words:
            # Check if adding the next word exceeds the line width
            test_line = word + " " + current_line if current_line else word
            line_width = draw.textlength(test_line, font=font)  # Use textlength for width calculation

            if line_width <= max_width:
                current_line = test_line
            else:
                # Draw the current line and move to the next line
                draw.text((10, y_position), current_line, fill="white", font=font, direction="rtl")
                y_position += line_height
                current_line = word

                # Stop if we run out of vertical space
                if y_position + line_height > device.height:
                    break

        # Draw the last line
        if current_line and y_position + line_height <= device.height:
            draw.text((10, y_position), current_line, fill="white", font=font, direction="rtl")

# Main function
def main():
    device = get_device()
    arabic_font = load_arabic_font()  # Load Arabic font
    # Start audio stream
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, device=None,
                            dtype="int16", channels=1, callback=callback):
        print("Listening... Speak into the microphone.")

        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                recognized_text = result["text"]
                print("Recognized:", recognized_text)

                # Display recognized Arabic text on OLED
                display_arabic_text(device, recognized_text, arabic_font)

if __name__ == "__main__":
    main()
