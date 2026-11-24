
from pathlib import Path
import csv

DATA_DIR = Path(r"D:\Database Homework\Data")

csv_files = sorted(DATA_DIR.glob("*.csv"))

headers = {}

for csv_file in csv_files:
    print(f"\n{'=' * 60}")
    print(f"FILE: {csv_file.name}")
    print("=" * 60)

    with open(csv_file, "r", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)

        header = next(reader)
        headers[csv_file.name] = header

        print(f"Number of columns: {len(header)}")
        print("\nColumns:")

        for i, column in enumerate(header, start=1):
            print(f"{i:2}. {column}")

        print("\nFirst 3 data rows:")
        for row in reader:
            print(row)
            if reader.line_num >= 4:
                break

# Compare headers
if len(headers) >= 2:
    header_list = list(headers.items())

    first_name, first_header = header_list[0]

    for name, header in header_list[1:]:
        print(f"\nComparing:")
        print(f"{first_name} vs {name}")

        if first_header == header:
            print("RESULT: Headers are identical.")
        else:
            print("RESULT: Headers are DIFFERENT.")
