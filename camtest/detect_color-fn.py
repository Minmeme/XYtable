import cv2
import numpy as np
import csv
from datetime import datetime
import time  # เพิ่มส่วนนี้

# กำหนดช่วงสี HSV สำหรับแต่ละสี
yellow_lower = np.array([15, 150, 20])
yellow_upper = np.array([35, 255, 255])

pink_lower = np.array([140, 50, 100])
pink_upper = np.array([170, 255, 255])

blue_lower = np.array([100, 100, 100])
blue_upper = np.array([130, 255, 255])

white_lower = np.array([0, 0, 200])
white_upper = np.array([180, 55, 255])

# เตรียมเขียนไฟล์ CSV
csv_filename = '/home/meme/Documents/cata/camtest/csv/color_counts.csv'
with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Timestamp', 'Yellow', 'Blue', 'Pink', 'White'])  # Header

# ตัวแปรสำหรับจับเวลา
last_save_time = time.time()

cap = cv2.VideoCapture(2)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    yellow_count = 0
    blue_count = 0
    pink_count = 0
    white_count = 0

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

    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    pink_mask = cv2.inRange(hsv, pink_lower, pink_upper)
    white_mask = cv2.inRange(hsv, white_lower, white_upper)

    yellow_count = detect_color(frame, yellow_mask, (0, 255, 255), "Yellow", 30)
    blue_count = detect_color(frame, blue_mask, (255, 0, 0), "Blue", 60)
    pink_count = detect_color(frame, pink_mask, (255, 0, 255), "Pink", 90)
    white_count = detect_color(frame, white_mask, (255, 255, 255), "White", 120)

    current_time = time.time()
    if (current_time - last_save_time >= 5) and (yellow_count > 0 or blue_count > 0 or pink_count > 0 or white_count > 0):
        with open(csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                yellow_count,
                blue_count,
                pink_count,
                white_count
            ])
        last_save_time = current_time  # อัปเดตเวลาล่าสุดที่บันทึก

    cv2.imshow('Detected Colors', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
