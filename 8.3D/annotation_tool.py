# annotation_tool.py

import os
import csv

def annotate_files():
    files = sorted([f for f in os.listdir() if f.endswith('.jpg')])
    annotations = []

    print("Annotate each image as:")
    print("[0] No activity\n[1] Activity 1 (e.g. waving)\n[2] Activity 2 (e.g. shaking)")

    for img_file in files:
        print(f"\nNow reviewing: {img_file}")
        os.system(f'start {img_file}' if os.name == 'nt' else f'xdg-open "{img_file}"')
        label = input("Enter label (0/1/2): ").strip()
        while label not in ['0', '1', '2']:
            label = input("Invalid input. Please enter 0, 1, or 2: ").strip()
        annotations.append((img_file.split('.')[0], label))

    with open("annotations.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "activity"])
        writer.writerows(annotations)

    print("Annotations saved to annotations.csv")

if __name__ == "__main__":
    annotate_files()
