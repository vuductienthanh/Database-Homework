from pathlib import Path
import csv
import time
import mysql.connector

# ==========================================
# CONFIGURATION
# ==========================================

DATA_DIR = Path(r"D:\Database Homework\Data")
CSV_FILE = DATA_DIR / "yellow_tripdata_2014-01.csv"

TEST_ROWS = 1000000

SAMPLE_FILE = DATA_DIR / f"sample_{TEST_ROWS}.csv"

# ==========================================
# CREATE SAMPLE CSV
# ==========================================

print(f"Preparing {TEST_ROWS} rows...")

with open(CSV_FILE, "r", encoding="utf-8", newline="") as source:
    reader = csv.reader(source)

    header = next(reader)

    with open(SAMPLE_FILE, "w", encoding="utf-8", newline="") as target:
        writer = csv.writer(target)

        writer.writerow(header)

        for i, row in enumerate(reader):
            if i >= TEST_ROWS:
                break

            writer.writerow(row)

print("Sample CSV created successfully!")

# ==========================================
# CONNECT TO DATABASE
# ==========================================

conn = mysql.connector.connect(
    host="127.0.0.1",
    port=3306,
    user="root",
    password="...",
    database="taxi_homework",
    allow_local_infile=True
)

cursor = conn.cursor()

# ==========================================
# CLEAN STAGING TABLE
# ==========================================

cursor.execute("DELETE FROM trips_staging")

# ==========================================
# LOAD DATA LOCAL INFILE
# ==========================================

sql = f"""
LOAD DATA LOCAL INFILE '{SAMPLE_FILE.as_posix()}'
INTO TABLE trips_staging
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\\n'
IGNORE 1 LINES
(
    VendorID,
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    passenger_count,
    trip_distance,
    RatecodeID,
    store_and_fwd_flag,
    PULocationID,
    DOLocationID,
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
"""

# ==========================================
# BENCHMARK
# ==========================================

start_time = time.perf_counter()

cursor.execute(sql)

elapsed_time = time.perf_counter() - start_time

print(f"Successfully loaded {TEST_ROWS} rows.")

print(f"Elapsed time: {elapsed_time:.2f} seconds")

# ==========================================
# ROLLBACK TEST DATA
# ==========================================

conn.rollback()

print("Rollback completed. Test data was not permanently saved.")

cursor.close()
conn.close()