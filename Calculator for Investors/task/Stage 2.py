import sqlite3
import csv
import os

# Reset database for each run
if os.path.exists("investor.db"):
    os.remove("investor.db")

# 1. Create database + connect
conn = sqlite3.connect("investor.db")
cur = conn.cursor()

# 2. Create tables
cur.execute("""
 CREATE TABLE IF NOT EXISTS companies (
     ticker TEXT primary key,
     name TEXT,
     sector TEXT
 )
""")

cur.execute("""
CREATE TABLE financial (
    ticker TEXT PRIMARY KEY,
    ebitda REAL,
    sales REAL,
    net_profit REAL,
    market_price REAL,
    net_debt REAL,
    assets REAL,
    equity REAL,
    cash_equivalents REAL,
    liabilities REAL
)
""")

# Helper: convert empty strings
def clean(value):
    if value == "" or value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return value


# 3. Populate companies table
with open("test/companies.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = [
        (r["ticker"], r["name"], r["sector"])
        for r in reader
    ]

cur.executemany("""
    INSERT INTO companies (ticker, name, sector)
    VALUES (?, ?, ?)
""", rows)

# 4. Populate financial table
with open("test/financial.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = [
        (
            r["ticker"],
            clean(r["ebitda"]),
            clean(r["sales"]),
            clean(r["net_profit"]),
            clean(r["market_price"]),
            clean(r["net_debt"]),
            clean(r["assets"]),
            clean(r["equity"]),
            clean(r["cash_equivalents"]),
            clean(r["liabilities"])
        )
        for r in reader
    ]


cur.executemany("""
    INSERT INTO financial (
        ticker, ebitda, sales, net_profit, market_price, net_debt,
        assets, equity, cash_equivalents, liabilities
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", rows)

# Finalize
conn.commit()
conn.close()

print("Database created successfully!")