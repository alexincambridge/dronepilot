# Python Script to Decode LD06 LiDAR Frames
# This script reads, parses, and displays distance measurements in real time.
#
# python
import serial
import struct

# Set up the serial connection serial0
SERIAL_PORT = "/dev/serial0"  # Use /dev/ttyS0 on some Raspberry Pi models
BAUD_RATE = 230400  # LD06 LiDAR default baud rate

def parse_lidar_data(data):
    """Parse the raw data frame from LD06 LiDAR and extract angles and distances."""
    if len(data) != 47 or data[0] != 0x54 or data[1] != 0x2C:
        return None  # Invalid frame

    speed = struct.unpack("<H", data[2:4])[0] / 100  # RPM
    timestamp = struct.unpack("<H", data[4:6])[0]  # Time in ms

    print(f"🌀 Speed: {speed} RPM | ⏱ Timestamp: {timestamp} ms")

    readings = []
    for i in range(12):  # 12 sets of angle-distance
        offset = 6 + (i * 3)
        angle_raw = struct.unpack("<H", data[offset : offset + 2])[0] / 100  # Degrees
        distance_raw = struct.unpack("<H", data[offset + 2 : offset + 4])[0]  # mm
        strength = data[offset + 4]  # Signal strength

        if 0 < distance_raw < 4000:  # Filter out bad readings
            readings.append((angle_raw, distance_raw))
            print(f"🔹 Angle: {angle_raw:.2f}° | 📏 Distance: {distance_raw} mm | 📶 Strength: {strength}")

    return readings

def read_lidar():
    """Continuously read and parse data from LiDAR."""
    try:
        with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as ser:
            buffer = bytearray()
            while True:
                byte = ser.read(1)  # Read byte-by-byte
                if not byte:
                    continue

                buffer.extend(byte)

                # Check if buffer has a full frame (47 bytes)
                if len(buffer) >= 47:
                    readings = parse_lidar_data(buffer[:47])
                    buffer = buffer[47:]  # Remove processed frame

    except serial.SerialException as e:
        print("⚠️ Serial Error:", e)
    except KeyboardInterrupt:
        print("\n🛑 Stopped by user.")

if __name__ == "__main__":
    print("🚀 Starting LD06 LiDAR Test...")
    read_lidar()