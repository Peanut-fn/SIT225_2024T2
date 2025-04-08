import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned data
df = pd.read_csv("gyroscope_data.csv")

# Plot x, y, z values separately
plt.figure(figsize=(10, 5))
plt.subplot(3, 1, 1)
plt.plot(df["timestamp"], df["x"], label="X-axis", color='r')
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(df["timestamp"], df["y"], label="Y-axis", color='g')
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(df["timestamp"], df["z"], label="Z-axis", color='b')
plt.legend()

plt.tight_layout()
plt.savefig("gyroscope_individual_axes.png")
plt.show()

# Plot all axes in one graph
plt.figure(figsize=(10, 5))
plt.plot(df["timestamp"], df["x"], label="X-axis", color='r')
plt.plot(df["timestamp"], df["y"], label="Y-axis", color='g')
plt.plot(df["timestamp"], df["z"], label="Z-axis", color='b')
plt.legend()
plt.title("Gyroscope Data Over Time")
plt.xlabel("Timestamp")
plt.ylabel("Values")
plt.savefig("gyroscope_combined_axes.png")
plt.show()