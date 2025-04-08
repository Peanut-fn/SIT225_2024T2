import pandas as pd
import matplotlib.pyplot as plt

# Load Cleaned Data
df = pd.read_csv("gyroscope_data_db2.csv")

# Plot x, y, z separately
plt.figure(figsize=(12, 6))
plt.subplot(3, 1, 1)
plt.plot(df["timestamp"], df["x"], label="X-axis", color="r")
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(df["timestamp"], df["y"], label="Y-axis", color="g")
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(df["timestamp"], df["z"], label="Z-axis", color="b")
plt.legend()

plt.xlabel("Timestamp")
plt.suptitle("Gyroscope Data (DB-2 - CouchDB)")
plt.xticks(rotation=45)
plt.show()

# Combined Plot
plt.figure(figsize=(10, 5))
plt.plot(df["timestamp"], df["x"], label="X-axis", color="r")
plt.plot(df["timestamp"], df["y"], label="Y-axis", color="g")
plt.plot(df["timestamp"], df["z"], label="Z-axis", color="b")

plt.xlabel("Timestamp")
plt.ylabel("Gyroscope Values")
plt.title("Gyroscope Data (DB-2 - CouchDB) - X, Y, Z")
plt.legend()
plt.xticks(rotation=45)
plt.show()