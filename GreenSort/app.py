from flask import Flask, render_template, Response, jsonify
import cv2
from cvzone.ClassificationModule import Classifier

app = Flask(__name__)
classifier = Classifier('Model/keras_model.h5', 'Model/labels.txt')
cap = cv2.VideoCapture(2)


@app.route('/video_feed')
def video_feed():
    def gen_frames():
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            prediction = classifier.getPrediction(frame)
            classID = prediction[1]
            label = get_label_and_strategy(classID)[0]
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                break
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
            return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/get_result')
def get_result():
    ret, frame = cap.read()
    if ret:
        prediction = classifier.getPrediction(frame)
        classID = prediction[1]
        label, strategy = get_label_and_strategy(classID)
        return jsonify({'label': label, 'strategy': strategy})
    return jsonify({'label': label, 'strategy': strategy})


def get_label_strategy(classID):
    categories = {
        1: ('Cardboard-Biodegradable', 'Recycle by composting or reusing.'),
        2: ('Glass-Solid Waste', 'Clean and place in the recycling bin for glass.'),
        3: ('Footwear-Textile Waste', 'Donate or Recycle through a textile recycling center.'),
        4: ('Cloth-Textile Waste', 'Donate or repurpose as cleaning rags.'),
        5: ('Metal-Non-Biodegradable', 'Recyle at a metal collection facility.'),
        6: ('Paper-Biodegradable', 'Recycle in the paper recycling bin or Reuse.'),
        7: ('Battery-Hazardous', 'Dispose at desginated battery recycling centres.'),
        8: ('Organic Waste-Biodegradable', 'Compost to create natural fertilizers.'),
        9: ('Toothbrush-Non-biodegradable', 'Reuse for kitchen purposes or place in non-recyclable waste.'),
        10: ('Diaper/Pads-Rejected Waste', 'Wrap and place in non-recyclable waste.'),
        11: ('Mask-Household Waste', 'Dispose of in household waste with proper containment.'),
        12: ('Plastic-Non-biodegradable', 'Check the type and recycle or dispose accordingly.'),
        13: ('Phone-E-Waste', 'Take to electronic recycling facility.')
    }
    return categories.get(classID, ('Unknown', 'No Recycling Strategy available.'))


@app.route("/")
def index():
    return render_template('greenindex.html')


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
