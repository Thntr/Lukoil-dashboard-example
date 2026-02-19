import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_fake_data(n=4000):
    """
    Generates a fake dataset for LUKOIL Strategic Dashboard v3.0.
    """
    np.random.seed(42)  # For reproducibility

    # 1. Brands (24 brands)
    brands = [
        "LUKOIL", "MOBIL", "CASTROL", "SHELL", "QUAKER STATE", "PENTOSIN",
        "AKRON", "ROSHFRANS", "BARDAHL", "TOTAL", "ELF", "MOTUL",
        "VALVOLINE", "REPSOL", "HAVOLINE", "GONHER", "MOTORCRAFT",
        "ACDELCO", "LUBRAL", "RALOY", "VISTONY", "GULF", "ENEOS", "IDEMITSU"
    ]

    # 2. Categories & Segments
    categories = ['PCMO', 'HDMO']
    product_types = ['Individual', 'Bundle']
    channels = ['Digital', 'Physical']
    regions = ['CDMX', 'Puebla']

    data = []

    # Dates for Q1 2026 (Jan 1 to Mar 31)
    start_date = datetime(2026, 1, 1)
    end_date = datetime(2026, 3, 31)
    delta_days = (end_date - start_date).days

    for _ in range(n):
        brand = np.random.choice(brands)
        category = np.random.choice(categories, p=[0.7, 0.3]) # 70% PCMO, 30% HDMO
        product_type = np.random.choice(product_types, p=[0.85, 0.15]) # Mostly individual items
        
        # Region: CDMX (70%), Puebla (30%)
        region = np.random.choice(regions, p=[0.7, 0.3])
        
        # Channel
        channel = np.random.choice(channels)

        # Base Price Logic ($120 - $1800)
        base_price = np.random.uniform(120, 1800)
        
        # Price Gap Logic: Physical is 5-12% higher than Digital
        if channel == 'Physical':
            price = base_price * np.random.uniform(1.05, 1.12)
        else:
            price = base_price
            
        # Date distribution
        random_days = random.randrange(delta_days)
        date = start_date + timedelta(days=random_days)
        
        # Fake Coordinates for Maps (Centered roughly on CDMX and Puebla)
        if region == 'CDMX':
            lat = np.random.uniform(19.25, 19.58)
            lon = np.random.uniform(-99.35, -98.95)
        else: # Puebla
            lat = np.random.uniform(18.98, 19.10)
            lon = np.random.uniform(-98.30, -98.10)

        record = {
            "Date": date,
            "Brand": brand,
            "Category": category,
            "Product_Type": product_type,
            "Channel": channel,
            "Region": region,
            "Price": round(price, 2),
            "Latitude": lat,
            "Longitude": lon,
            "SKU_Name": f"{brand} {category} {product_type} {random.randint(1, 100)}"
        }
        data.append(record)

    df = pd.DataFrame(data)
    
    # Calculate Price Gap Column (Simulated for display)
    # This is a bit tricky since we have individual rows, but for the KPI we can aggregate later.
    # For now, let's just ensure the 'Price' column reflects the logic.
    
    return df

def get_kpi_metrics(df):
    """
    Calculates high-level KPIs from the dataframe.
    """
    total_items = len(df)
    brands_count = df['Brand'].nunique()
    avg_price = df['Price'].mean()
    
    # Calculate approximate digital/physical gap
    avg_physical = df[df['Channel'] == 'Physical']['Price'].mean()
    avg_digital = df[df['Channel'] == 'Digital']['Price'].mean()
    
    if avg_digital > 0:
        gap_percent = ((avg_physical - avg_digital) / avg_digital) * 100
    else:
        gap_percent = 0
        
    return total_items, brands_count, avg_price, gap_percent