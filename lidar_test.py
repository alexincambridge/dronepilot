# Python Script to Read LiDAR Data
# This script reads raw LiDAR data from /dev/serial0 (UART0) and prints the output:
#
# python
import serial
import struct

# Set up the serial connection
SERIAL_PORT = "/dev/serial0"  # Use /dev/ttyS0 on some models
BAUD_RATE = 230400  # LD06 LiDAR default baud rate

def read_lidar():
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            while True:
                data = ser.read(32)  # Read a chunk of data
                if data:
                    print("Received Data:", data.hex())  # Print raw hex values
    except serial.SerialException as e:
        print("Serial Error:", e)
    except KeyboardInterrupt:
        print("\nStopped by user")

if __name__ == "__main__":
    print("Starting LiDAR Test...")
    read_lidar()