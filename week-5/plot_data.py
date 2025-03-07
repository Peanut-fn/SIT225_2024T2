import pandas as pd
import matplotlib.pyplot as plt

# Load Data
df = pd.read_csv("gyroscope_data.csv")

# Plot X, Y, Z values
plt.figure(figsize=(10, 5))

plt.subplot(3, 1, 1)
plt.plot(df["X"], label="X-axis", color="r")
plt.legend()

plt.subplot(3, 1, 2)
plt.plot(df["Y"], label="Y-axis", color="g")
plt.legend()

plt.subplot(3, 1, 3)
plt.plot(df["Z"], label="Z-axis", color="b")
plt.legend()

plt.xlabel("Samples")
plt.ylabel("Gyroscope Values")
plt.suptitle("Gyroscope Readings Over Time")
plt.show()
