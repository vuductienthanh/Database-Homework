
import csv
import time
from pathlib import Path
import mysql.connector

# ==============================
# CONFIGURATION
# ==============================

DATA_DIR = Path(r"D:\Database Homework\Data")
CSV_FILE = DATA_DIR / "yellow_tripdata_2014-01.csv"

TEST_ROWS = 500000
BATCH_SIZE = 1000

# ==============================
# CONNECT TO DATABASE
# ==============================

conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="...",
    database="taxi_homework"
)

cursor = conn.cursor()

# ==============================
# SQL INSERT STATEMENT
# ==============================

insert_sql = """
INSERT INTO trips (
    vendor_id,
    pickup_datetime,
    dropoff_datetime,
    passenger_count,
    trip_distance,
    ratecode_id,
    store_and_fwd_flag,
    pickup_location_id,
    dropoff_location_id,
    payment_type,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    improvement_surcharge,
    total_amount,
    congestion_surcharge,
    airport_fee
)
VALUES (
    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
    %s, %s, %s, %s, %s, %s, %s, %s, %s
)
"""

# ==============================
# READ CSV & BATCH INSERT
# ==============================

batch = []
inserted_rows = 0

start_time = time.perf_counter()

try:
    with open(CSV_FILE, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:

            values = (
                row["VendorID"] or None,
                row["tpep_pickup_datetime"] or None,
                row["tpep_dropoff_datetime"] or None,
                row["passenger_count"] or None,
                row["trip_distance"] or None,
                row["RatecodeID"] or None,
                row["store_and_fwd_flag"] or None,
                row["PULocationID"] or None,
                row["DOLocationID"] or None,
                row["payment_type"] or None,
                row["fare_amount"] or None,
                row["extra"] or None,
                row["mta_tax"] or None,
                row["tip_amount"] or None,
                row["tolls_amount"] or None,
                row["improvement_surcharge"] or None,
                row["total_amount"] or None,
                row["congestion_surcharge"] or None,
                row["airport_fee"] or None
            )

            batch.append(values)

            if len(batch) >= BATCH_SIZE:
                cursor.executemany(insert_sql, batch)
                inserted_rows += len(batch)
                batch.clear()

            if inserted_rows + len(batch) >= TEST_ROWS:
                break

        # Insert remaining rows in the final batch
        if batch:
            remaining = TEST_ROWS - inserted_rows

            if remaining > 0:
                batch = batch[:remaining]
                cursor.executemany(insert_sql, batch)
                inserted_rows += len(batch)

    elapsed_time = time.perf_counter() - start_time

    print(f"Successfully inserted {inserted_rows} test rows.")
    print("Test data was not permanently saved.")
    print(f"Batch size: {BATCH_SIZE}")
    print(f"Elapsed time: {elapsed_time:.2f} seconds")

finally:
    conn.rollback()
    cursor.close()
    conn.close()

    print("Rollback completed. Test data was not permanently saved.")
