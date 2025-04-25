import serial
import socket
import time

# Server config
HOST = '10.10.199.124'  # Server IP
PORT = 5000            # Port

# Serial config
SERIAL_PORT = '/dev/ttyUSB0'  # เปลี่ยนตามพอร์ตที่ใช้จริง
BAUDRATE = 9600               # ต้องตรงกับอุปกรณ์ปลายทาง
ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)

def connect_to_server():
    global client_socket, Button
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((HOST, PORT))
        
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            Button = data.decode('utf-8').strip()
            print(Button)

            command_map = {
                'A': 0x01,
                'B': 0x02,
                'X': 0x03,
                'Y': 0x04,
                'R1': 0x05,
                'R2': 0x06,
                'L1': 0x07,
                'L2': 0x09,
                'Hat_Up': 0x10,
                'Hat_Down': 0x11,
                'Hat_L': 0x12,
                'Hat_R': 0x13,
                'ButtonLX1': 0x14,
                'ButtonLX-1': 0x15,
                'ButtonLY1': 0x16,
                'ButtonLY-1': 0x17,
                'ButtonRX1': 0x18,
                'ButtonRX-1': 0x19,
                'ButtonRY1': 0x20,
                'ButtonRY-1': 0x21,
                # 'LYDown_and_RYDown': 0x24,
                # 'LYUp_and_RYUp': 0x25,
                # 'LYDown_and_RYUp': 0x26,
                # 'LYUp_and_RYDown': 0x27,
                'ButtonL': 0x28,
                'ButtonR': 0x29,
                'Stop': 0xFF,  # คุณสามารถเปลี่ยนค่าตรงนี้ได้ตามต้องการ
            }

            if Button in command_map:
                byte_to_send = command_map[Button]
                ser.write(bytes([byte_to_send]))
                print(f"Sent: {hex(byte_to_send)}")

    except Exception as e:
        print("An error occurred:", e)

connect_to_server()
