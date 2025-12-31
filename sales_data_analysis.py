import pandas as pd

# ---------- 1. Load data ----------
orders = pd.read_csv("Orders.csv")
details = pd.read_csv("Details.csv")

print("Orders columns:", orders.columns.tolist())
print("Details columns:", details.columns.tolist())

print("\nOrders shape:", orders.shape)
print("Details shape:", details.shape)

# ---------- 2. Standardize key column name ----------
if "Order ID" in orders.columns:
    orders = orders.rename(columns={"Order ID": "OrderID"})

# ---------- 3. Quick preview ----------
print("\nOrders head:")
print(orders.head())

print("\nDetails head:")
print(details.head())

# ---------- 4. Merge orders and details ----------
merged = pd.merge(details, orders, on="OrderID", how="inner")

print("\nMerged shape:", merged.shape)
print("\nMerged head:")
print(merged.head())

# ---------- 5. Basic sales metrics ----------
amount_col_candidates = ["Sales", "Amount", "Total", "TotalAmount"]
amount_col = None
for c in amount_col_candidates:
    if c in merged.columns:
        amount_col = c
        break

if amount_col is None and {"Qty", "UnitPrice"}.issubset(set(merged.columns)):
    merged["TotalAmount"] = merged["Qty"] * merged["UnitPrice"]
    amount_col = "TotalAmount"

if amount_col is not None:
    print(f"\nUsing '{amount_col}' as total sales amount column.")

    total_sales = merged[amount_col].sum()
    print(f"\nTotal sales amount: {total_sales:.2f}")

    sales_by_state = (
        merged.groupby("State")[amount_col]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    print("\nTop 10 states by sales:")
    print(sales_by_state)

    sales_by_city = (
        merged.groupby("City")[amount_col]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )
    print("\nTop 10 cities by sales:")
    print(sales_by_city)

else:
    print("\nCould not find a total amount column.")
    print("Please make sure Details.csv has either:")
    print("- a 'Sales' / 'Amount' / 'Total' column, OR")
    print("- both 'Qty' and 'UnitPrice' columns so TotalAmount can be computed.")
