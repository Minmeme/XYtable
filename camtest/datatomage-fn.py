import csv
import time
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600) 

# ฟังก์ชั่นเพื่ออ่านไฟล์ CSV ทีละบรรทัดและเช็คว่าเป็นสีอะไรบ้าง
def monitor_csv_with_colors(csv_file, known_lines):
    while True:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # ข้ามแถว header

            new_data_found = False
            for line in reader:
                # เช็คว่าบรรทัดนี้มีข้อมูลใหม่หรือไม่
                if line not in known_lines:
                    known_lines.append(line)  # เพิ่มข้อมูลใหม่ลงใน known_lines
                    timestamp = line[0]
                    colors = []
                    
                    # ตรวจสอบค่าของแต่ละสีในบรรทัดนั้น
                    if line[1] == '1':
                        colors.append('Yellow')
                        ser.write('yellow\n')
                    if line[2] == '1':
                        colors.append('Blue')
                        ser.write('Blue\n')
                    if line[3] == '1':
                        colors.append('Pink')
                        ser.write('Pink\n')
                    if line[4] == '1':
                        colors.append('White')
                        ser.write('white\n')

                    # แสดงผลข้อมูลใหม่พร้อมสี
                    if colors:
                        print(f"new data (Timestamp: {timestamp}): {', '.join(colors)}")
                    else:
                        print(f"new (Timestamp: {timestamp}): no color")
                    new_data_found = True

            if not new_data_found:
                print("No new data.")

        # รอ 5 วินาที ก่อนตรวจสอบไฟล์อีกครั้ง
        time.sleep(5)

# กำหนดชื่อไฟล์ CSV ของคุณ
csv_file = '/home/meme/Documents/cata/camtest/csv/color_counts.csv'

# สร้าง list สำหรับเก็บข้อมูลที่เคยอ่านแล้ว
known_lines = []

# เรียกใช้ฟังก์ชั่นเพื่อตรวจสอบข้อมูลใหม่
monitor_csv_with_colors(csv_file, known_lines)
