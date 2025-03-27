import subprocess
import os

# Define your custom text variable
#text = "noise Hello world, this is a test on the medium quality."
text= "مرحبا مرحبا هذا هو فريق إيشارا"

# Path to the directory containing the piper executable
piper_dir = "/home/pi/Desktop/piper/piper"

# Change the working directory to the one containing the piper executable
os.chdir(piper_dir)
#model = 'en-us-blizzard_lessac-medium.onnx'
model = 'ar_JO-kareem-medium.onnx'
# Create the shell command
command = f"echo '{text}' | ./piper --model {model} --output_file welcome.wav"

# Run the shell command
subprocess.run(command, shell=True, check=True)


# Play the generated welcome.wav file using aplay
play_command = "aplay welcome.wav"

# Run the command to play the wav file
subprocess.run(play_command, shell=True, check=True)
