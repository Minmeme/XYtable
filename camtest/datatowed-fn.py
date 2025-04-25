import csv
import time
import os
from datetime import datetime

# ฟังก์ชั่นเขียนผลรวมสีลงในไฟล์ CSV พร้อม id และ timestamp
def write_totals_to_csv(output_file, yellow, blue, pink, white, record_id):
    file_exists = os.path.isfile(output_file)

    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['ID', 'Timestamp', 'Yellow_Total', 'Blue_Total', 'Pink_Total', 'White_Total'])

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([record_id, timestamp, yellow, blue, pink, white])

# ฟังก์ชันหลัก ตรวจสอบไฟล์ต้นทางและอัปเดตไฟล์ผลรวม
def monitor_and_add_by_color(csv_file, known_lines, output_file):
    yellow_total = 0
    blue_total = 0
    pink_total = 0
    white_total = 0
    record_id = 1  # เริ่ม ID จาก 1

    while True:
        with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # ข้าม header

            new_data_found = False
            for line in reader:
                if line not in known_lines:
                    known_lines.append(line)
                    print(f"ข้อมูลใหม่: {line}")
                    new_data_found = True

                    try:
                        yellow = int(line[1])
                        blue = int(line[2])
                        pink = int(line[3])
                        white = int(line[4])

                        yellow_total += yellow
                        blue_total += blue
                        pink_total += pink
                        white_total += white

                        print(f"ผลรวม Yellow: {yellow_total}")
                        print(f"ผลรวม Blue: {blue_total}")
                        print(f"ผลรวม Pink: {pink_total}")
                        print(f"ผลรวม White: {white_total}")

                        # เขียนผลรวมลงไฟล์ CSV ใหม่พร้อม ID และเวลา
                        write_totals_to_csv(output_file, yellow_total, blue_total, pink_total, white_total, record_id)
                        record_id += 1

                    except ValueError:
                        print("ข้อมูลไม่ถูกต้องในบรรทัดนี้")

            if not new_data_found:
                print("ไม่มีข้อมูลใหม่.")

        time.sleep(5)

# ตั้งค่าชื่อไฟล์
csv_file = '/home/meme/Documents/cata/camtest/csv/color_counts.csv'
output_csv = '/home/meme/Documents/cata/camtest/csv/color_totals.csv'
known_lines = []

# เรียกฟังก์ชัน
monitor_and_add_by_color(csv_file, known_lines, output_csv)
