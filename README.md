# Hand-Gesture LED Control

Turning LEDs on based on hand gestures.

Using a webcam, the number of fingers raised is detected, and the LEDs are turned on accordingly.

## Python
OpenCV is used to capture video from the webcam. MediaPipe provides hand-tracking capabilities that are used to count the number of fingers raised. The serial library is used to send the detected data to the Arduino through serial communication.

## Arduino
Five LEDs are connected to digital pins 8 through 12, with 220-ohm resistors placed in between. The Arduino receives the data sent from Python, stores it in a variable, and uses it to determine how many LEDs should be turned on.

## How It Works

1. The webcam captures live video.
2. MediaPipe detects a hand and tracks its landmarks.
3. The Python program estimates how many fingers are raised.
4. The count is displayed on the screen and sent to the Arduino.
5. The Arduino turns on the corresponding number of LEDs.
