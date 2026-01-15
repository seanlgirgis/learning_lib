import csv
import random
import datetime
import uuid

# Configuration
NUM_ROWS = 100_000
OUTPUT_FILE = "large_sales_data.csv"

# Sample Data Elements
CITIES = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"]
PRODUCTS = [
    {"name": "Laptop Pro", "base_price": 1200},
    {"name": "Smartphone X", "base_price": 800},
    {"name": "Headphones NoiseCancel", "base_price": 250},
    {"name": "4K Monitor", "base_price": 400},
    {"name": "Mechanical Keyboard", "base_price": 150},
    {"name": "Wireless Mouse", "base_price": 50},
    {"name": "USB-C Hub", "base_price": 40},
    {"name": "Gaming Chair", "base_price": 300},
]
PAYMENT_METHODS = ["Credit Card", "PayPal", "Debit Card", "Apple Pay"]

def random_date(start_year=2024, end_year=2026):
    start = datetime.datetime(start_year, 1, 1)
    end = datetime.datetime(end_year, 1, 1)
    return start + (end - start) * random.random()

print(f"Generating {NUM_ROWS} rows of synthetic data...")

with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    # Header
    writer.writerow([
        "transaction_id", 
        "customer_id", 
        "customer_name", 
        "transaction_date", 
        "city", 
        "product_name", 
        "quantity", 
        "unit_price", 
        "total_amount", 
        "payment_method"
    ])

    for i in range(NUM_ROWS):
        product = random.choice(PRODUCTS)
        qty = random.choices([1, 2, 3, 4, 5], weights=[0.7, 0.2, 0.05, 0.03, 0.02])[0]
        # Add some random variance to price (discounts, etc)
        price = round(product["base_price"] * random.uniform(0.9, 1.1), 2)
        total = round(price * qty, 2)
        
        writer.writerow([
            str(uuid.uuid4()), # transaction_id
            f"CUST-{random.randint(1000, 5000)}", # customer_id (simulating repeat customers)
            f"Customer_{random.randint(1, 1000)}", # customer_name
            random_date().strftime("%Y-%m-%d %H:%M:%S"),
            random.choice(CITIES),
            product["name"],
            qty,
            price,
            total,
            random.choice(PAYMENT_METHODS)
        ])
        
        if (i + 1) % 10000 == 0:
            print(f"Generated {i + 1} rows...")

print(f"Done! File saved to: {OUTPUT_FILE}")
