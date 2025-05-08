import time
import pandas as pd
import cv2
from datetime import datetime
import random  

DEVICE_ID = "959e8c91-3315-4c12-b62f-28435c73436a"
SECRET_KEY = "YUGis@TpbWqWQi#@9#Tk4xhbt" 

def get_accel_data():
    """
    Replace this with the actual method you used in 8.1P to receive real-time data.
    For now, simulated data is returned.
    """
    return random.uniform(-10, 10), random.uniform(-10, 10), random.uniform(-10, 10)

def capture_image(filename):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(filename, frame)
    cap.release()

def save_data_and_image(x_data, y_data, z_data, sequence):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    base_filename = f"{sequence}_{timestamp}"
    df = pd.DataFrame({'x': x_data, 'y': y_data, 'z': z_data})
    df.to_csv(f"{base_filename}.csv", index=False)
    capture_image(f"{base_filename}.jpg")
    print(f"Saved: {base_filename}.csv and .jpg")
    return base_filename

def run_collection(duration_minutes=30):
    sequence = 1
    end_time = time.time() + duration_minutes * 60

    while time.time() < end_time:
        x_data, y_data, z_data = [], [], []
        start = time.time()

        while time.time() - start < 10:
            accel = get_accel_data()
            if accel:
                x, y, z = accel
                x_data.append(x)
                y_data.append(y)
                z_data.append(z)
            time.sleep(0.5)

        save_data_and_image(x_data, y_data, z_data, sequence)
        sequence += 1

if __name__ == "__main__":
    run_collection(duration_minutes=30)
