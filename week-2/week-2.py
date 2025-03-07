import pandas as pd
import matplotlib.pyplot as plt

filename = "Sumit.csv"
df = pd.read_csv(filename)

# Display the first few rows to verify the 'Time' column
print(df.head())

# Ensure 'Time' column is treated as a string and remove invalid headers if needed
df = df[df['Time'].astype(str).str.isnumeric()]  # Keep only numeric time values

# Convert 'Time' to datetime format, handling errors
df['Timestamp'] = pd.to_datetime(df['Time'], format="%Y%m%d%H%M%S", errors='coerce')

# Drop NaN values if conversion fails
df = df.dropna(subset=['Timestamp'])

# Extract numeric values from 'Distance in (cm)' column
df['Distance in (cm)'] = df['Distance in (cm)'].astype(str).str.extract(r'(\d+)').astype(float)

# Apply rolling average smoothing
df['Smoothed_Distance'] = df['Distance in (cm)'].rolling(window=5, min_periods=1).mean()

# Plot the smoothed data
plt.figure(figsize=(12, 6))
plt.plot(df['Timestamp'], df['Smoothed_Distance'], markersize=1, linestyle='-', color='b')
plt.xlabel('Time')
plt.ylabel('Distance (cm)')
plt.title('Ultrasonic Sensor Readings (Smoothed)')
plt.xticks(rotation=45)
plt.grid(True)
plt.show()