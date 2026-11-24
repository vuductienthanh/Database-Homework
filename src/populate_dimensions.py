from pathlib import Path
import csv
import mysql.connector

DATA_DIR = Path(r"D:\Database Homework\Data")

CSV_FILES = sorted(DATA_DIR.glob("*.csv"))

conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="...",
    database="taxi_homework"
)

cursor = conn.cursor()

vendors = set()
payment_types = set()
rate_codes = set()

for csv_file in CSV_FILES:
    print(f"Reading: {csv_file.name}")

    with open(csv_file, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:

            vendor = row["VendorID"]
            payment = row["payment_type"]
            rate = row["RatecodeID"]

            if vendor.strip():
                vendors.add(int(vendor))

            if payment.strip():
                payment_types.add(int(payment))

            if rate.strip():
                rate_codes.add(int(rate))

print("\nUnique values found:")
print("Vendors:", vendors)
print("Payment types:", payment_types)
print("Rate codes:", rate_codes)

cursor.executemany(
    "INSERT IGNORE INTO vendors (vendor_id) VALUES (%s)",
    [(v,) for v in vendors]
)

cursor.executemany(
    "INSERT IGNORE INTO payment_types (payment_type_id) VALUES (%s)",
    [(p,) for p in payment_types]
)

cursor.executemany(
    "INSERT IGNORE INTO rate_codes (rate_code_id) VALUES (%s)",
    [(r,) for r in rate_codes]
)

conn.commit()

print("\nDimension tables populated successfully!")

cursor.close()
conn.close()