# Solution Stage 2
Below is a polished, production‑ready Python script that:
* creates investor.db
* creates both tables
* loads CSVs
* converts empty values to None
* converts numeric fields to floats
* inserts data
* prints final success message

## ✅ Complete Python Script (clean, correct, ready to run)
```python
import sqlite3
import csv

# -----------------------------
# 1. Create database + connect
# -----------------------------
conn = sqlite3.connect("investor.db")
cur = conn.cursor()

# -----------------------------
# 2. Create tables
# -----------------------------
cur.execute("""
CREATE TABLE companies (
    ticker TEXT PRIMARY KEY,
    name   TEXT,
    sector TEXT
)
""")

cur.execute("""
CREATE TABLE financial (
    ticker TEXT PRIMARY KEY,
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

# -----------------------------
# Helper: convert empty strings
# -----------------------------
def clean(value):
    if value == "" or value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return value

# -----------------------------
# 3. Populate companies table
# -----------------------------
with open("./test/companies.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = [
        (r["ticker"], r["name"], r["sector"])
        for r in reader
    ]

cur.executemany("""
    INSERT INTO companies (ticker, name, sector)
    VALUES (?, ?, ?)
""", rows)

# -----------------------------
# 4. Populate financial table
# -----------------------------
with open("./test/financial.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = [
        (
            r["ticker"],
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
        ticker, sales, net_profit, market_price, net_debt,
        assets, equity, cash_equivalents, liabilities
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
""", rows)

# -----------------------------
# Finalize
# -----------------------------
conn.commit()
conn.close()

print("Database created successfully!")
```

## Which folder, will investor.db be created?
It goes exactly where your Python script is running from — nothing more mysterious than that.

SQLite doesn’t create hidden folders or system paths.
If your script contains:4
```markdown
conn = sqlite3.connect("investor.db")
```
then investor.db  will appear in the same directory where you executed the script.

A quick way to think about it
* If you run the script from VS Code, it appears in the folder opened in the Explorer panel.
* If you run it from a terminal, it appears in the terminal’s current working directory (`pwd` on macOS/Linux, `cd` on Windows).
* If you run it from PyCharm, it appears in the project root unless you changed the working directory.

### Want to verify?
Add this tiny snippet:
```markdown
import os
print("Working directory:", os.getcwd())
```
That path is where investor.db will be created.

## In SQL isn’t request for "None" to insert "NULL" as value to column?
In SQLite (and in Python’s `sqlite3` module), `None` is exactly the correct way to insert SQL `NULL`.
You never write `"NULL"` as a string — that would literally insert the text `"NULL"` into the column.

### How it works
- Python value `None` → SQLite stores `NULL`
- Python value ` "" ` (empty string) → SQLite stores an **empty string**, **not NULL**
- Python value ` "NULL" ` → SQLite stores the text `"NULL"` (wrong)

So your cleaning function:
```markdown
def clean(value):
    if value == "" or value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return value
```
is doing exactly the right thing.
When `executemany()` runs, SQLite sees `None` and inserts a real SQL `NULL`.

**Quick demonstration**
```markdown
cur.execute("INSERT INTO financial (ticker, sales) VALUES (?, ?)", ("AAPL", None))
```
SQLite stores:

| ticker | sales |
|--------|-------|
| AAPL   | NULL  |

**Why this works**  

**The Python DB‑API (PEP 249) defines a direct mapping:**

| Python | SQLite  |
|--------|---------|
| None   | NULL    |
| float  | REAL    |
| int    | INTEGER |
| str    | TEXT    |

So you never need to write SQL like:
```markdown
INSERT INTO table VALUES (NULL)
```
Python handles it automatically.