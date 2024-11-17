import serial
from flask import Flask, render_template
import serial
import time
import threading
import cv2
import serial.tools.list_ports

app = Flask(__name__)
arduino = serial.Serial('COM5', 115200, timeout=1)
try: 
    global co_value_global
    print("Connected!")
    while True:
        line = arduino.readline().decode('utf-8').strip()
        if line:
            print(f"Received: {line}")
            co_value_global = int(line.split(":")[1].strip())
except serial.SerialException as e:
    print(f"Serial Error: {e}")
@app.route("/")
def index():
    return render_template("Emitech.html", value=co_value_global)
serial_thread = threading.Thread(target=read_serial_data, daemon=True)
serial_thread.start()
if __name__ == "__main__":
    app.run(debug=True)