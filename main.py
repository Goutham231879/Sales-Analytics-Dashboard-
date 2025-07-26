
import pandas as pd
import sqlite3
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sb
import os

# =========================
# Load CSV into SQLite DB
# =========================
csv_path = "data/retail_sales_dataset.csv"
db_path = "sales.db"

# Make sure CSV exists
if not os.path.exists(csv_path):
    st.error(f"CSV file not found at {csv_path}")
else:
    # Read CSV and clean column names
    df = pd.read_csv(csv_path, parse_dates=["Date"])
    df.columns = df.columns.str.strip()  # remove any trailing spaces

    # Save to SQLite
    with sqlite3.connect(db_path) as conn:
        df.to_sql("sales", conn, if_exists="replace", index=False)

# =========================
# Streamlit Dashboard
# =========================
st.title("📊 Sales Analytics Dashboard")

# Connect to SQLite
conn = sqlite3.connect(db_path)

# --- Monthly Revenue ---
monthly_sales = pd.read_sql("""
    SELECT strftime('%Y-%m', Date) AS Month, SUM(Total) AS Revenue
    FROM sales
    GROUP BY Month
    ORDER BY Month
""", conn)

# --- Top Products by Revenue ---
top_products = pd.read_sql("""
    SELECT Product, SUM(Total) AS Revenue
    FROM sales
    GROUP BY Product
    ORDER BY Revenue DESC
    LIMIT 5
""", conn)

conn.close()

# =========================
# Visualizations
# =========================

# --- Monthly Revenue Trend ---
st.subheader("Monthly Revenue Trend")
fig, ax = plt.subplots()
sb.lineplot(data=monthly_sales, x="Month", y="Revenue", marker="o", ax=ax)
plt.xticks(rotation=45)
plt.ylabel("Revenue")
plt.xlabel("Month")
st.pyplot(fig)

# --- Top 5 Products by Revenue ---
st.subheader("Top 5 Products by Revenue")
st.bar_chart(top_products.set_index("Product"))
