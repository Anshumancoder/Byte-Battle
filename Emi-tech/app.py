import random
from flask import Flask, render_template
import serial
import threading
import cv2
import time
import cv2

def capture_picture(output_filename="captured_image.jpg"):
    cap = cv2.VideoCapture(0)  
    if not cap.isOpened():
        return "Error: Could not access the camera."    
    ret, frame = cap.read()
    if ret:
        save_path = "C:/Users/saura/OneDrive/Documents/GitHub/Byte-Battlesss/Emi-tech/static/" + output_filename
        cv2.imwrite(save_path, frame)
        print(f"Image saved to {save_path}.")
    else:
        print("Error: Could not capture an image.")    
    cap.release()
capture_picture("captured_image.jpg")
co_value_global=None

def read_sensor_data():
    try: 
        arduino = serial.Serial('COM5', 115200, timeout=1)
        global co_value_global
        print("Connected!")
        while True:
            print("crosscheck", co_value_global)
            line = arduino.readline().decode('utf-8').strip()
            if not line:  # Ignore empty lines
                continue
            print(f"Received: {line}")
            if line.startswith("CO value:"):
                try:
                    co_value_global = int(line.split(":")[1].strip())
                    print(f"Updated CO Value: {co_value_global}")
                    if co_value_global >= 43:
                        print("Threshold exceeded. Capturing picture...")
                        arduino.close()
                        capture_picture()
                        arduino.open()
                except ValueError:
                    print(f"Error parsing CO value from: {line}")
            elif line.startswith("Limit:"):
                print(f"Received limit message: {line}")
            else:
                print(f"Invalid data format. Skipping: {line}")
    except Exception as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("Exiting serial reading...")




app = Flask(__name__)

@app.route("/")
def index():
    return render_template("Emitech.html", val=co_value_global)

if __name__ == "__main__":
    sensor_thread = threading.Thread(target=read_sensor_data)
    sensor_thread.daemon = True
    sensor_thread.start()
    app.run()
