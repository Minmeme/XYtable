import cv2
import numpy as np
import csv
import time
from datetime import datetime
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit
import threading

app = Flask(__name__)
socketio = SocketIO(app)

# HSV สีที่ต้องการตรวจจับ
yellow_lower = np.array([15, 150, 20])
yellow_upper = np.array([35, 255, 255])
pink_lower = np.array([140, 50, 100])
pink_upper = np.array([170, 255, 255])
blue_lower = np.array([100, 100, 100])
blue_upper = np.array([130, 255, 255])
white_lower = np.array([0, 0, 200])
white_upper = np.array([180, 55, 255])

# เส้นทาง CSV
csv_file = '/home/meme/Documents/cata/camtest/csv/color_counts.csv'

# เตรียมเขียน header ถ้ายังไม่มีไฟล์
try:
    with open(csv_file, mode='x', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Timestamp', 'Yellow', 'Blue', 'Pink', 'White'])
except FileExistsError:
    pass

cap = cv2.VideoCapture(0)
last_save_time = time.time()
last_data = ['-', 0, 0, 0, 0]

def detect_color(frame, mask, color_bgr, label_text, y_offset):
    count = 0
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        if cv2.contourArea(cnt) > 500:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x+w, y+h), color_bgr, 2)
            count += 1
    cv2.putText(frame, f"{label_text}: {count}", (400, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color_bgr, 2)
    return count

def gen_frames():
    global last_save_time, last_data
    while True:
        success, frame = cap.read()
        if not success:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
        blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
        pink_mask = cv2.inRange(hsv, pink_lower, pink_upper)
        white_mask = cv2.inRange(hsv, white_lower, white_upper)

        yellow_count = detect_color(frame, yellow_mask, (0, 255, 255), "Yellow", 30)
        blue_count = detect_color(frame, blue_mask, (255, 0, 0), "Blue", 60)
        pink_count = detect_color(frame, pink_mask, (255, 0, 255), "Pink", 90)
        white_count = detect_color(frame, white_mask, (255, 255, 255), "White", 120)

        current_time = time.time()
        if current_time - last_save_time >= 5:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            with open(csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, yellow_count, blue_count, pink_count, white_count])
            last_data = [timestamp, yellow_count, blue_count, pink_count, white_count]
            last_save_time = current_time

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        

# ฟังก์ชันเพื่ออ่านข้อมูลจาก CSV
def get_last_row():
    csv_file = '/home/meme/Documents/cata/camtest/csv/color_totals.csv'
    last_row = None
    try:
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = list(csv.reader(file))
            if len(reader) > 1:
                last_row = reader[-1]  # แถวล่าสุด (ID, Timestamp, Yellow, Blue, Pink, White)
    except FileNotFoundError:
        last_row = None
    return last_row

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('get_data')
def send_data():
    last_row = get_last_row()
    emit('update_data', {'totals': last_row})
         
def check_csv_updates():
    while True:
        socketio.sleep(5)  # เช็คทุกๆ 5 วินาที
        last_row = get_last_row()
        socketio.emit('update_data', {'totals': last_row}, to=None)

if __name__ == "__main__":
    socketio.start_background_task(check_csv_updates)
    socketio.run(app, host='0.0.0.0', port=5050)
