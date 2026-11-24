from pathlib import Path
import csv
import mysql.connector
import time

DATA_DIR = Path(r"D:\Database Homework\Data")

CSV_FILE = DATA_DIR / "yellow_tripdata_2014-01.csv"

TEST_ROWS = 10000

conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="...",
    database="taxi_homework"
)

cursor = conn.cursor()

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

start_time = time.time()

inserted = 0

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

            cursor.execute(insert_sql, values)

            inserted += 1

            if inserted >= TEST_ROWS:
                break

    print(f"Successfully inserted {inserted} test rows.")

    conn.rollback()

    print("Rollback completed. Test data was not permanently saved.")

except Exception as e:
    conn.rollback()
    print("Error:", e)

finally:
    elapsed_time = time.time() - start_time

    print(f"Elapsed time: {elapsed_time:.2f} seconds")

    cursor.close()
    conn.close()