import cv2
# from . import client
from flask import Flask, render_template, Response
from multiprocessing import Process

app = Flask(__name__)

cap = cv2.VideoCapture(0) # wedcam
# cap = cv2.VideoCapture(0) # pi camera

count = 0

def gen_frames():
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# def gen_frames1():
#     while True:
#         success, frame = cap1.read()
#         if not success:
#             break
#         else:
#             ret, buffer = cv2.imencode('.jpg', frame)
#             frame = buffer.tobytes()
#             yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# @app.route('/video_feed1')
# def video_feed1():
#     return Response(gen_frames1(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__== "__main__":
    app.run(host='10.10.199.124', port=5050, threaded=True ,debug=False) # use Pi_pi
    # joy = Process(target=client.connect_to_server)
    # joy.start()
