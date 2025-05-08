import serial
import csv
import time

# --- Configuration ---
SERIAL_PORT = 'COM18'  # Replace with your Arduino's serial port (e.g., 'COM3' on Windows)
BAUD_RATE = 9600
CSV_FILENAME = 'dht11_data.csv'
COLLECTION_DURATION_SECONDS = 1200  # Collect data for 30 minutes (30 * 60 seconds)
SAMPLE_INTERVAL_SECONDS = 5       # Read data every 5 seconds

# --- Initialize lists to store data ---
temperatures = []
humidities = []
start_time = time.time()

try:
    # --- Establish serial connection ---
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    print(f"Connected to serial port {SERIAL_PORT} at {BAUD_RATE} baud.")

    # --- Collect data for the specified duration ---
    print(f"Collecting data for {COLLECTION_DURATION_SECONDS} seconds...")
    while time.time() - start_time < COLLECTION_DURATION_SECONDS:
        try:
            # --- Read a line from the serial port ---
            line = ser.readline().decode('utf-8').strip()

            if line:
                print(f"Received: {line}")
                if "Temperature:" in line and "Humidity:" in line:
                    try:
                        # --- Extract temperature and humidity values ---
                        temperature_str = line.split("Temperature: ")[1].split(" *C")[0].strip()
                        humidity_str = line.split("Humidity: ")[1].split(" %")[0].strip()

                        temperature = float(temperature_str)
                        humidity = float(humidity_str)

                        temperatures.append(temperature)
                        humidities.append(humidity)
                        print(f"Extracted: Temperature={temperature:.2f}°C, Humidity={humidity:.2f}%")
                    except (ValueError, IndexError) as e:
                        print(f"Error parsing data: {e} - Line: {line}")

            time.sleep(SAMPLE_INTERVAL_SECONDS)

        except serial.SerialException as e:
            print(f"Error reading from serial port: {e}")
            break

except serial.SerialException as e:
    print(f"Could not open serial port {SERIAL_PORT}: {e}")

finally:
    # --- Close the serial port ---
    if 'ser' in locals() and ser.is_open:
        ser.close()
        print("Serial port closed.")

    # --- Save data to CSV file ---
    if temperatures and humidities:
        with open(CSV_FILENAME, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Temperature', 'Humidity'])  # Write header row
            for i in range(len(temperatures)):
                csv_writer.writerow([temperatures[i], humidities[i]])
        print(f"Data saved to {CSV_FILENAME}")
    else:
        print("No data collected to save.")