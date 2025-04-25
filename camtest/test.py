import cv2
import numpy as np

# กำหนดช่วงสี HSV สำหรับแต่ละสี
yellow_lower = np.array([15, 150, 20])
yellow_upper = np.array([35, 255, 255])

pink_lower = np.array([140, 50, 100])
pink_upper = np.array([170, 255, 255])

blue_lower = np.array([100, 100, 100])
blue_upper = np.array([130, 255, 255])

white_lower = np.array([0, 0, 200])
white_upper = np.array([180, 55, 255])

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # แปลงภาพเป็น HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Reset เคานต์ทุกสีในทุกเฟรม
    yellow_count = 0
    blue_count = 0
    pink_count = 0
    white_count = 0

    # ฟังก์ชันสำหรับการ detect สี
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


    # สร้าง masks
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    pink_mask = cv2.inRange(hsv, pink_lower, pink_upper)
    white_mask = cv2.inRange(hsv, white_lower, white_upper)

    # นับและแสดงผลแต่ละสี
    yellow_count = detect_color(frame, yellow_mask, (0, 255, 255), "Yellow", 30)
    blue_count = detect_color(frame, blue_mask, (255, 0, 0), "Blue", 60)
    # pink_count = detect_color(frame, pink_mask, (255, 0, 255), "Pink", 90)
    # white_count = detect_color(frame, white_mask, (255, 255, 255), "White", 120)    


    # แสดงภาพ
    cv2.imshow('Detected Colors', frame)

    # ออกจากลูปเมื่อกด 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
