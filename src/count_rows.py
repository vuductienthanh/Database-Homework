from pathlib import Path

DATA_DIR = Path(r"D:\Database Homework\Data")

for csv_file in DATA_DIR.glob("*.csv"):
    print(f"Counting: {csv_file.name}")

    with open(csv_file, "r", encoding="utf-8") as f:
        row_count = sum(1 for _ in f) - 1

    print(f"{csv_file.name}: {row_count:,} rows\n")

print("Counting completed!")