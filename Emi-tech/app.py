from flask import Flask, render_template
import serial
import time
import threading
import cv2
app = Flask(__name__)

# Flask Route
@app.route("/")
def index():
    return render_template("Emitech.html")


def capture_picture(output_filename="captured_image.jpg"):

    # Initialize the webcam (device index 0 by default)
    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        return "Error: Could not access the camera."

    # Capture a single frame
    ret, frame = cap.read()
    if ret:
        # Save the captured frame to a file
        cv2.imwrite(output_filename, frame)
        result = f"Image saved to {output_filename}."
    else:
        result = "Error: Could not capture an image."

    # Release the camera
    cap.release()
    return result

# Example usage
if __name__ == "__main__":
    print(capture_picture("my_picture.jpg"))

# Setup serial communication
arduino = serial.Serial('COM5', 115200)  # Change this to the correct port on your system
time.sleep(2)  # Give the Arduino time to reset

def read_serial_data():
    try:
        while True:
            # Read data from the Arduino
            line = arduino.readline().decode('utf-8').strip()

            if line.startswith("CO value:"):
                co_value = line.split(":")[1].strip()
                print(f"CO value: {co_value}")

            elif line.startswith("Limit:"):
                limit = line.split(":")[1].strip()
                print(f"Limit: {limit}")

            time.sleep(5)  # Wait for 5 seconds before reading again

    except KeyboardInterrupt:
        print("Exiting serial reading...")
    
    finally:
        arduino.close()  # Close the serial connection

# Start the serial reading in a separate thread
serial_thread = threading.Thread(target=read_serial_data, daemon=True)
serial_thread.start()
capture_picture()
if __name__ == "__main__":
    app.run()
