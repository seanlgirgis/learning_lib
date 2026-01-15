"""
Refactored Horizon Data Loader (Generator Pattern)
--------------------------------------------------
Scenario: HorizonScale needs to process 5TB of historical metric logs.
Problem: Loading 5TB into a Pandas DataFrame crashes the server (OOM).
Solution: Use a Python Generator to 'stream' the file line-by-line.

Author: Sean Luka Girgis (Senior Data Engineer)
"""

import csv
import time
import random
import os
import psutil  # To show memory usage proof

# Mock File Configuration
MOCK_FILE = "large_horizon_metrics.csv"
TOTAL_ROWS = 1_000_000  # Simulating a large file (1 million lines)

def get_memory_usage():
    """Returns current memory usage of this process in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def generate_mock_data(filename, row_count):
    """
    Creates a dummy CSV file to simulate raw telemetry logs.
    Format: timestamp, server_id, cpu_usage, memory_usage
    """
    print(f"Creating mock data file: {filename} with {row_count} rows...")
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "server_id", "cpu_usage", "memory_usage"])
        
        # Write rows efficiently
        for _ in range(row_count):
            writer.writerow([
                time.time(),
                f"server-{random.randint(1, 1000)}",
                random.uniform(10.0, 99.9),
                random.uniform(2.0, 32.0)
            ])
    print("Mock data generation complete.\n")

def lazy_metric_loader(file_path):
    """
    THE GENERATOR: Yields one row at a time.
    Crucially, it opens the file and keeps a cursor, never loading the whole thing.
    """
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # We can even do light transformation here "on the fly"
            row['cpu_usage'] = float(row['cpu_usage'])
            row['memory_usage'] = float(row['memory_usage'])
            yield row  # <--- The Magic Word: Returns control but saves state

def process_metrics_pipeline(loader):
    """
    The Consumer: Iterates over the generator.
    Memory usage should remain FLAT and LOW, regardless of file size.
    """
    print(f"Starting pipeline. Initial Memory: {get_memory_usage():.2f} MB")
    
    count = 0
    max_cpu = 0.0
    
    start_time = time.time()
    
    # Iterate over the generator (streaming)
    for record in loader:
        count += 1
        
        # Simple 'reduce' logic
        if record['cpu_usage'] > max_cpu:
            max_cpu = record['cpu_usage']
        
        # Proof of life every 100k rows
        if count % 100_000 == 0:
            print(f"Processed {count} rows. Current Memory: {get_memory_usage():.2f} MB")
            
    end_time = time.time()
    
    print("-" * 30)
    print(f"PIPELINE COMPLETE")
    print(f"Total Rows: {count}")
    print(f"Max CPU Found: {max_cpu:.2f}")
    print(f"Time Taken: {end_time - start_time:.2f} seconds")
    print(f"Final Memory: {get_memory_usage():.2f} MB")
    print(f"VERDICT: Memory stayed low because we streamed the data!")

if __name__ == "__main__":
    # 1. Setup Data
    if not os.path.exists(MOCK_FILE):
        generate_mock_data(MOCK_FILE, TOTAL_ROWS)
        
    # 2. Initialize Generator
    # Note: This function call is nearly instant. It returns an iterator, doesn't process data yet.
    my_generator = lazy_metric_loader(MOCK_FILE)
    
    # 3. Run Pipeline
    process_metrics_pipeline(my_generator)
    
    # Cleanup
    if os.path.exists(MOCK_FILE):
        os.remove(MOCK_FILE)
