import pandas as pd

# Load data
orders = pd.read_csv("Orders.csv")
details = pd.read_csv("Details.csv")

print("Orders shape:", orders.shape)
print("Details shape:", details.shape)

print("\nOrders head:")
print(orders.head())

print("\nDetails head:")
print(details.head())

# Merge on OrderID (change if your key name is different)
merged = pd.merge(details, orders, on="OrderID", how="inner")
print("\nMerged shape:", merged.shape)
print(merged.head())
