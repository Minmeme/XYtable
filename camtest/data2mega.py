import csv
import time
import serial

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1) 

def get_new_colors(csv_file, known_lines):
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # ข้าม header

        for line in reader:
            if line not in known_lines:
                known_lines.append(line)
                timestamp = line[0]
                colors = []

                if line[1] == '1':
                    colors.append('yellow')
                if line[2] == '1':
                    colors.append('blue')
                if line[3] == '1':
                    colors.append('pink')
                if line[4] == '1':
                    colors.append('white')

                return (timestamp, colors)
    return (None, [])

csv_file = '/home/meme/Documents/cata/camtest/csv/color_counts.csv'
known_lines = []

print("ระบบพร้อม รอ IR Trigger จาก Arduino...")

while True:
    timestamp, colors = get_new_colors(csv_file, known_lines)

    if colors:
        print(f"เตรียมส่งข้อมูลสีจาก Timestamp {timestamp}: {', '.join(colors)}")

        while True:
            if ser.in_waiting > 0:
                incoming = ser.readline().decode().strip()
                print("Arduino:", incoming)

                if "IR" in incoming:
                    for color in colors:
                        ser.write((color + '\n').encode())
                        print(f"ส่ง: {color}")

                        # รอ Arduino ตอบกลับ "OK"
                        while True:
                            if ser.in_waiting > 0:
                                response = ser.readline().decode().strip()
                                print(f"Arduino ตอบกลับ: {response}")
                                if response == "OK":
                                    break
                    break  # ออกจาก loop รอ IR

    else:
        print("ยังไม่มีข้อมูลใหม่")

    time.sleep(2)
