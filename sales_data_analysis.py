import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# ========== 1. LOAD DATA ==========
print("\n" + "="*60)
print("DATA ANALYSIS PROJECT - SALES & ORDERS ANALYSIS")
print("="*60 + "\n")

try:
    orders = pd.read_csv("Orders.csv")
    details = pd.read_csv("Details.csv")
    print("SUCCESS: Data files loaded!\n")
except FileNotFoundError as e:
    print(f"ERROR: {e}")
    print("Please ensure Orders.csv and Details.csv are in the same directory.")
    exit()

print(f"Orders: {orders.shape[0]} rows, {orders.shape[1]} columns")
print(f"Details: {details.shape[0]} rows, {details.shape[1]} columns")

# ========== 2. DATA CLEANING & STANDARDIZATION ==========
print("\n" + "="*60)
print("CLEANING & STANDARDIZATION")
print("="*60 + "\n")

if "Order ID" in orders.columns:
    orders = orders.rename(columns={"Order ID": "OrderID"})
    print("Standardized: Order ID -> OrderID")

if "Order ID" in details.columns:
    details = details.rename(columns={"Order ID": "OrderID"})
    print("Standardized: Order ID -> OrderID in details")

print(f"Missing values - Orders: {orders.isnull().sum().sum()}")
print(f"Missing values - Details: {details.isnull().sum().sum()}")

# ========== 3. MERGE DATA ==========
print("\n" + "="*60)
print("MERGING ORDERS & DETAILS")
print("="*60 + "\n")

if "OrderID" not in orders.columns or "OrderID" not in details.columns:
    print("ERROR: OrderID column not found")
    exit()

merged = pd.merge(details, orders, on="OrderID", how="inner")
print(f"Merged shape: {merged.shape}")
print(f"Total records: {len(merged):,}")
print(f"Total columns: {len(merged.columns)}")

# ========== 4. CALCULATE SALES AMOUNT ==========
print("\n" + "="*60)
print("CALCULATING SALES METRICS")
print("="*60 + "\n")

amount_col = None
amount_col_candidates = ["Sales", "Amount", "Total", "TotalAmount"]

for col in amount_col_candidates:
    if col in merged.columns:
        amount_col = col
        print(f"Found amount column: '{amount_col}'")
        break

if amount_col is None:
    if "Qty" in merged.columns and "UnitPrice" in merged.columns:
        merged["TotalAmount"] = merged["Qty"] * merged["UnitPrice"]
        amount_col = "TotalAmount"
        print("Calculated TotalAmount = Qty * UnitPrice")
    else:
        print(f"ERROR: Cannot find amount column. Available: {list(merged.columns)}")
        exit()

# ========== 5. SALES ANALYSIS ==========
print("\n" + "="*60)
print("SALES ANALYSIS")
print("="*60 + "\n")

if amount_col:
    total_sales = merged[amount_col].sum()
    print(f"Total Sales Amount: {total_sales:,.2f}\n")
    
    print("Sales Statistics:")
    print(f"  Mean: {merged[amount_col].mean():,.2f}")
    print(f"  Median: {merged[amount_col].median():,.2f}")
    print(f"  Std Dev: {merged[amount_col].std():,.2f}")
    print(f"  Min: {merged[amount_col].min():,.2f}")
    print(f"  Max: {merged[amount_col].max():,.2f}")
    
    if "State" in merged.columns:
        print("\n" + "-"*60)
        print("TOP 10 STATES BY SALES")
        print("-"*60 + "\n")
        sales_by_state = (
            merged.groupby("State")[amount_col]
            .agg(["sum", "count"])
            .rename(columns={"sum": "Total_Sales", "count": "Orders"})
            .sort_values("Total_Sales", ascending=False)
            .head(10)
        )
        print(sales_by_state)
    
    if "City" in merged.columns:
        print("\n" + "-"*60)
        print("TOP 10 CITIES BY SALES")
        print("-"*60 + "\n")
        sales_by_city = (
            merged.groupby("City")[amount_col]
            .agg(["sum", "count"])
            .rename(columns={"sum": "Total_Sales", "count": "Orders"})
            .sort_values("Total_Sales", ascending=False)
            .head(10)
        )
        print(sales_by_city)
    
    if "Category" in merged.columns:
        print("\n" + "-"*60)
        print("SALES BY CATEGORY")
        print("-"*60 + "\n")
        sales_by_category = (
            merged.groupby("Category")[amount_col]
            .sum()
            .sort_values(ascending=False)
        )
        print(sales_by_category)
    
    if "Profit" in merged.columns:
        print("\n" + "-"*60)
        print("PROFIT ANALYSIS")
        print("-"*60 + "\n")
        total_profit = merged["Profit"].sum()
        profit_margin = (total_profit / total_sales) * 100
        print(f"Total Profit: {total_profit:,.2f}")
        print(f"Profit Margin: {profit_margin:.2f}%")
        
        print("\nProfit by Category:")
        profit_by_category = merged.groupby("Category")["Profit"].sum().sort_values(ascending=False)
        for cat, profit in profit_by_category.items():
            print(f"  {cat}: {profit:,.2f}")

else:
    print("ERROR: Could not find or calculate sales amount column.")

print("\n" + "="*60)
print("ANALYSIS COMPLETE")
print("="*60)
