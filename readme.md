
# Project eveCV - EIA Asimov, Semillero Robótica
Robot capable of performing object detection using a Raspberry Pi Zero 2W and a camera module. The goal is to detect and track the user's presence in the camera feed.

![<alt_text>](<portrait.png>)

### Usage
This project consist in two folders. /robot for the robot code and /model for the ultralitics model. 

Run the file runModelMQTT.py with the right camera port and then run main.py in your raspberry pi. Make sure you got your environment correctly setup.

### Hardware
- Raspberry Pi Zero 2W
- Camera module compatible with Raspberry Pi
- MicroSD card (8GB or larger)
- Power supply for Raspberry Pi
- Wheels, motors, and chassis for the robot
- Breadboard and jumper wires for circuit connections

### Software
- Raspbian or Raspberry Pi OS installed on the Raspberry Pi
- Python 3
- TensorFlow Lite
- OpenCV
- GPIO Zero
