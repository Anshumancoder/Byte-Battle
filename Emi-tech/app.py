from flask import Flask, render_template
import serial
import time
import threading
import cv2

app = Flask(__name__)


co_value_global = None


arduino = serial.Serial('COM5', 115200)  
time.sleep(2)  


def read_serial_data():
    global co_value_global
    try:
        while True:
         
            line = arduino.readline().decode('utf-8').strip()

            if line.startswith("CO value:"):
                co_value_global = int(line.split(":")[1].strip()) 
                print(f"CO value (inside if): {co_value_global}")

                
               

            elif line.startswith("Limit:"):
                limit = line.split(":")[1].strip()
                print(f"Limit: {limit}")

            time.sleep(1)  

    except KeyboardInterrupt:
        print("Exiting serial reading...")

    finally:
        arduino.close()  


@app.route("/")
def index():
    return render_template("Emitech.html", value=co_value_global)


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


serial_thread = threading.Thread(target=read_serial_data, daemon=True)
serial_thread.start()


if __name__ == "__main__":
    app.run(debug=True)
