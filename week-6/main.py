import serial
import pandas as pd
import time
import csv

SERIAL_PORT = 'COM18' 
BAUD_RATE = 115200
CSV_FILENAME = "gyro.csv"

# Open Serial Connection
ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
time.sleep(2)  # Allow time for the connection to establish

# Create CSV file and write the header
with open(CSV_FILENAME, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["timestamp", "gyro_x", "gyro_y", "gyro_z"])  # Writing column headers

print(f" {CSV_FILENAME} created. Now collecting data... (Press Ctrl+C to stop)")

try:
    with open(CSV_FILENAME, mode='a', newline='') as file:  # Open in append mode
        writer = csv.writer(file)

        while True:
            line = ser.readline().decode('utf-8').strip()  # Read and decode serial data

            if line and "timestamp" not in line:  # Ignore header line
                try:
                    timestamp, gx, gy, gz = map(float, line.split(','))  # Convert data to float
                    writer.writerow([timestamp, gx, gy, gz])  # Write data to CSV file

                    # Print real-time data to console
                    print(f"Timestamp: {timestamp}, Gyro_X: {gx}, Gyro_Y: {gy}, Gyro_Z: {gz}")

                except ValueError:
                    pass  # Ignore errors in parsing data

except KeyboardInterrupt:
    print("\n Data collection stopped.")
    ser.close()  # Close serial connection
    print(f" Data saved in {CSV_FILENAME}.")