import serial

# Serial config
SERIAL_PORT = '/dev/ttyUSB0'  # เปลี่ยนตามพอร์ตที่ใช้จริง
BAUDRATE = 9600               # ต้องตรงกับอุปกรณ์ปลายทาง
ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=1)

# Map ของคำสั่ง -> byte
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
    'ButtonL': 0x28,
    'ButtonR': 0x29,
    'Stop': 0xFF,
}

def main():
    print("Ready. Type a command or 'exit' to quit.")
    while True:
        command = input("Enter command: ").strip()
        if command.lower() == 'exit':
            break
        if command in command_map:
            byte_to_send = command_map[command]
            ser.write(bytes([byte_to_send]))
            print(f"Sent: {hex(byte_to_send)}")
        else:
            print("Unknown command.")

if __name__ == '__main__':
    main()
