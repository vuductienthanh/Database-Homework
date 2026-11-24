
from pathlib import Path
import pyarrow.parquet as pq

DATA_DIR = Path(r"D:\Database Homework\Data")

parquet_files = list(DATA_DIR.glob("*.parquet"))

for parquet_file in parquet_files:
    csv_file = parquet_file.with_suffix(".csv")

    print(f"Converting: {parquet_file.name}")

    parquet_reader = pq.ParquetFile(parquet_file)

    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        first_batch = True

        for batch in parquet_reader.iter_batches(batch_size=100_000):
            batch_df = batch.to_pandas()

            batch_df.to_csv(
                f,
                index=False,
                header=first_batch
            )

            first_batch = False

    print(f"Completed: {csv_file.name}")

print("All files converted!")
