import csv
import firebase_admin
from firebase_admin import credentials, db

# Firebase Initialization
firebase_config_file = "dct-tasks-2-0-firebase-adminsdk-fbsvc-824b5cf816.json"
firebase_db_url = "https://dct-tasks-2-0-default-rtdb.asia-southeast1.firebasedatabase.app/"

try:
    firebase_admin.get_app()  # Check if Firebase is already initialized
except ValueError:
    credentials_file = credentials.Certificate(firebase_config_file)
    firebase_admin.initialize_app(credentials_file, {"databaseURL": firebase_db_url})

# Reference Firebase Data
data_reference = db.reference("gyroscope_data")
gyro_data = data_reference.get()

# Save Data to CSV
csv_filename = "gyroscope_data.csv"

if gyro_data:
    try:
        with open(csv_filename, "w", newline="", encoding="utf-8") as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["Timestamp", "X", "Y", "Z"])  # CSV Headers

            for record_id, record in gyro_data.items():
                csv_writer.writerow([record["timestamp"], record["x"], record["y"], record["z"]])

        print(f"Data successfully saved to {csv_filename}")

    except Exception as file_error:
        print(f"Error writing to CSV: {file_error}")

else:
    print("No gyroscope data found in Firebase.")
