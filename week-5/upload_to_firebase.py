import serial
import json
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Firebase setup
firebase_credentials = credentials.Certificate("dct-tasks-2-0-firebase-adminsdk-fbsvc-824b5cf816.json")
firebase_admin.initialize_app(firebase_credentials, {
    "databaseURL": "https://dct-tasks-2-0-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

# Initialize serial connection
serial_port = "COM20"
baud_rate = 115200

try:
    with serial.Serial(serial_port, baud_rate) as ser:
        print("Listening for gyroscope data...")

        while True:
            try:
                # Read and process incoming data
                raw_data = ser.readline().decode("utf-8").strip()
                time_stamp, axis_x, axis_y, axis_z = raw_data.split(",")

                # Structure the data
                gyro_record = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "x": float(axis_x),
                    "y": float(axis_y),
                    "z": float(axis_z),
                }

                # Push to Firebase
                db.reference("gyroscope_data").push(gyro_record)
                print("Data uploaded:", gyro_record)

            except ValueError:
                print("Warning: Invalid data received, skipping...")
            except Exception as err:
                print("Unexpected error:", err)

except serial.SerialException:
    print("Failed to connect to serial port. Check the device connection.")
