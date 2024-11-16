import serial
from flask import Flask, render_template
import serial
import time

import cv2
import serial.tools.list_ports

def capture_picture(output_filename="captured_image.jpg"):
    cap = cv2.VideoCapture(1)  
    if not cap.isOpened():
        return "Error: Could not access the camera."
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(output_filename, frame)
        print(f"Image saved to {output_filename}.")
    else:
        print("Error: Could not capture an image.")
    cap.release()
arduino = serial.Serial('COM5', 115200, timeout=1)

try: 
    global co_value_global
    print("Connected!")
    while True:
        print(1)
        line = arduino.readline().decode('utf-8').strip()
        if line:
            print(2)
            print(f"Received: {line}")
            print(3)
            co_value_global = int(line.split(":")[1].strip())
            print(4)
            if co_value_global>=45:
                arduino.close()
                capture_picture()
                arduino.open()

except KeyboardInterrupt:
        print("Exiting serial reading...")
    



