import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

# Config
N = 4000
cities = ["Mumbai", "Pune", "Nagpur", "Nashik", "Thane", "Aurangabad"]
suppliers = ["Shenzhen Traders", "Guangzhou Imports", "Dragon Supply Co", "Yiwu Global Trade"]
categories = {
    "LED Lights": {"import": (180, 420), "sell": (450, 950), "supplier_bias": ["Shenzhen Traders", "Dragon Supply Co"]},
    "Mobile Accessories": {"import": (80, 250), "sell": (199, 599), "supplier_bias": ["Guangzhou Imports", "Yiwu Global Trade"]},
    "Smart Watches": {"import": (650, 1800), "sell": (1499, 4299), "supplier_bias": ["Shenzhen Traders", "Guangzhou Imports"]},
    "Bluetooth Speakers": {"import": (350, 900), "sell": (799, 2199), "supplier_bias": ["Dragon Supply Co", "Shenzhen Traders"]},
    "Kitchen Gadgets": {"import": (120, 380), "sell": (299, 899), "supplier_bias": ["Yiwu Global Trade", "Guangzhou Imports"]},
    "Home Decor": {"import": (90, 320), "sell": (249, 749), "supplier_bias": ["Yiwu Global Trade", "Dragon Supply Co"]},
}

# City demand weights (Mumbai highest)
city_weights = {"Mumbai": 0.30, "Pune": 0.22, "Thane": 0.18, "Nagpur": 0.13, "Nashik": 0.10, "Aurangabad": 0.07}

# Supplier delay profiles (days)
supplier_delays = {
    "Shenzhen Traders": {"mean": 4, "std": 2, "damage_rate": 0.04},
    "Guangzhou Imports": {"mean": 6, "std": 3, "damage_rate": 0.07},
    "Dragon Supply Co": {"mean": 9, "std": 5, "damage_rate": 0.12},
    "Yiwu Global Trade": {"mean": 3, "std": 1, "damage_rate": 0.03},
}

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

rows = []
for i in range(1, N + 1):
    # Random date with seasonal boost (Oct-Dec festival season)
    days_range = (end_date - start_date).days
    day_offset = np.random.randint(0, days_range)
    order_date = start_date + timedelta(days=int(day_offset))
    month = order_date.month
    seasonal_boost = 1.4 if month in [10, 11, 12] else (1.1 if month in [7, 8] else 1.0)

    product = random.choice(list(categories.keys()))
    cfg = categories[product]
    supplier = random.choice(cfg["supplier_bias"])
    delay_cfg = supplier_delays[supplier]

    city = random.choices(list(city_weights.keys()), weights=list(city_weights.values()))[0]

    import_cost = round(random.uniform(*cfg["import"]), 2)
    selling_price = round(import_cost * random.uniform(1.8, 3.2), 2)

    # Quantity: more in high-demand cities + seasonal boost
    base_qty = int(np.random.exponential(4)) + 1
    qty = max(1, int(base_qty * seasonal_boost * (1.3 if city == "Mumbai" else 1.0)))

    delay_days = max(0, int(np.random.normal(delay_cfg["mean"], delay_cfg["std"])))
    delivery_date = order_date + timedelta(days=delay_days)

    damaged = random.random() < delay_cfg["damage_rate"]
    if damaged:
        selling_price = round(selling_price * 0.7, 2)  # markdown

    profit = round((selling_price - import_cost) * qty, 2)

    rows.append({
        "Order_ID": f"ORD{str(i).zfill(5)}",
        "Product_Name": product,
        "Category": product,
        "City": city,
        "Supplier": supplier,
        "Import_Cost": import_cost,
        "Selling_Price": selling_price,
        "Quantity_Sold": qty,
        "Shipment_Delay_Days": delay_days,
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Delivery_Date": delivery_date.strftime("%Y-%m-%d"),
        "Profit": profit,
        "Damaged_Goods": damaged,
        "Month": month,
        "Year": order_date.year,
    })

df = pd.DataFrame(rows)
df.to_csv("/home/claude/China2MarketAI/data/sales_data.csv", index=False)
print(f"✅ Dataset generated: {len(df)} rows")
print(f"\nShape: {df.shape}")
print(f"\nColumn Types:\n{df.dtypes}")
print(f"\nSample:\n{df.head(3).to_string()}")
print(f"\nCity distribution:\n{df['City'].value_counts()}")
print(f"\nSupplier distribution:\n{df['Supplier'].value_counts()}")
print(f"\nTotal Revenue: ₹{(df['Selling_Price'] * df['Quantity_Sold']).sum():,.0f}")
print(f"Total Profit: ₹{df['Profit'].sum():,.0f}")
