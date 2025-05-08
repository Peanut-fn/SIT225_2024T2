# pattern_analysis.py

import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

def analyze_file(file):
    df = pd.read_csv(file)
    x, y, z = df['x'], df['y'], df['z']
    std_x, std_y, std_z = np.std(x), np.std(y), np.std(z)
    print(f"{file}: std_x={std_x:.2f}, std_y={std_y:.2f}, std_z={std_z:.2f}")

    df.plot(title=file)
    plt.xlabel("Sample Index")
    plt.ylabel("Acceleration")
    plt.legend(["X", "Y", "Z"])
    plt.grid(True)
    plt.show()

def analyze_all():
    files = sorted([f for f in os.listdir() if f.endswith('.csv')])
    for f in files:
        analyze_file(f)

if __name__ == "__main__":
    analyze_all()
