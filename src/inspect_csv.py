from pathlib import Path
import csv

DATA_DIR = Path(r"D:\Database Homework\Data")

for csv_file in DATA_DIR.glob("*.csv"):
    print(f"\nFile: {csv_file.name}")

    with open(csv_file, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        header = next(reader)

        for i, column in enumerate(header, start=1):
            print(f"{i}. {column}")

    print("-" * 50)