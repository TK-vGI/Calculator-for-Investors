import sqlite3
import csv
import os

DB_NAME = "investor.db"

MAIN_MENU = """MAIN MENU
0 Exit
1 CRUD operations
2 Show top ten companies by criteria
"""

CRUD_MENU = """CRUD MENU
0 Back
1 Create a company
2 Read a company
3 Update a company
4 Delete a company
5 List all companies
"""

TOP_TEN_MENU = """TOP TEN MENU
0 Back
1 List by ND/EBITDA
2 List by ROE
3 List by ROA
"""


def clean(value):
    if value == "" or value is None:
        return None
    try:
        return float(value)
    except ValueError:
        return value


def load_csv_data(cur):
    if os.path.exists("companies.csv"):
        with open("companies.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = [(r["ticker"], r["name"], r["sector"]) for r in reader]
            cur.executemany(
                "INSERT INTO companies (ticker, name, sector) VALUES (?, ?, ?)",
                rows
            )

    if os.path.exists("financial.csv"):
        with open("financial.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter="\t")
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
            cur.executemany(
                """
                INSERT INTO financial (
                    ticker, ebitda, sales, net_profit, market_price, net_debt,
                    assets, equity, cash_equivalents, liabilities
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                rows
            )


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            ticker TEXT PRIMARY KEY,
            name   TEXT,
            sector TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS financial (
            ticker           TEXT PRIMARY KEY,
            ebitda           REAL,
            sales            REAL,
            net_profit       REAL,
            market_price     REAL,
            net_debt         REAL,
            assets           REAL,
            equity           REAL,
            cash_equivalents REAL,
            liabilities      REAL
        )
    """)

    cur.execute("SELECT COUNT(*) FROM companies")
    count = cur.fetchone()[0]

    if count == 0:
        load_csv_data(cur)
        conn.commit()

    return conn, cur


def print_main_menu():
    print(MAIN_MENU)
    print("Enter an option:")


def print_crud_menu():
    print()
    print(CRUD_MENU)
    print("Enter an option:")


def print_top_ten_menu():
    print()
    print(TOP_TEN_MENU)
    print("Enter an option:")


def create_company(cur, conn):
    ticker = input("Enter ticker (in the format 'MOON'):\n")
    name = input("Enter company (in the format 'Moon Corp'):\n")
    sector = input("Enter industries (in the format 'Technology'):\n")

    ebitda = clean(input("Enter ebitda (in the format '987654321'):\n"))
    sales = clean(input("Enter sales (in the format '987654321'):\n"))
    net_profit = clean(input("Enter net profit (in the format '987654321'):\n"))
    market_price = clean(input("Enter market price (in the format '987654321'):\n"))
    net_debt = clean(input("Enter net debt (in the format '987654321'):\n"))
    assets = clean(input("Enter assets (in the format '987654321'):\n"))
    equity = clean(input("Enter equity (in the format '987654321'):\n"))
    cash_equivalents = clean(input("Enter cash equivalents (in the format '987654321'):\n"))
    liabilities = clean(input("Enter liabilities (in the format '987654321'):\n"))

    cur.execute(
        "INSERT INTO companies (ticker, name, sector) VALUES (?, ?, ?)",
        (ticker, name, sector)
    )

    cur.execute("""
        INSERT INTO financial (
            ticker, ebitda, sales, net_profit, market_price, net_debt,
            assets, equity, cash_equivalents, liabilities
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (ticker, ebitda, sales, net_profit, market_price, net_debt,
          assets, equity, cash_equivalents, liabilities))

    conn.commit()
    print("Company created successfully!")
    print()


def find_companies_by_name(cur, name):
    cur.execute(
        "SELECT ticker, name FROM companies WHERE name LIKE ?",
        (f"%{name}%",)
    )
    return cur.fetchall()


def choose_company(cur):
    name = input("Enter company name:\n")
    matches = find_companies_by_name(cur, name)

    if not matches:
        print("Company not found!")
        print()
        return None

    for idx, (_, cname) in enumerate(matches):
        print(f"{idx} {cname}")
    num = int(input("Enter company number:\n"))
    return matches[num][0], matches[num][1]


def format_ratio(value):
    if value is None:
        return None
    return float(f"{value:.2f}")


def read_company(cur):
    result = choose_company(cur)
    if result is None:
        return
    ticker, name = result

    cur.execute("""
        SELECT ebitda, sales, net_profit, market_price, net_debt,
               assets, equity, cash_equivalents, liabilities
        FROM financial
        WHERE ticker = ?
    """, (ticker,))
    row = cur.fetchone()

    if row is None:
        print("Company not found!")
        print()
        return

    ebitda, sales, net_profit, market_price, net_debt, assets, equity, cash_eq, liabilities = row

    pe = format_ratio(market_price / net_profit) if net_profit not in (None, 0) else None
    ps = format_ratio(market_price / sales) if sales not in (None, 0) else None
    pb = format_ratio(market_price / assets) if assets not in (None, 0) else None
    nd_ebitda = format_ratio(net_debt / ebitda) if ebitda not in (None, 0) else None
    roe = format_ratio(net_profit / equity) if equity not in (None, 0) else None
    roa = format_ratio(net_profit / assets) if assets not in (None, 0) else None
    la = format_ratio(liabilities / assets) if assets not in (None, 0) else None

    print(f"{ticker} {name}")
    print(f"P/E = {pe}")
    print(f"P/S = {ps}")
    print(f"P/B = {pb}")
    print(f"ND/EBITDA = {nd_ebitda}")
    print(f"ROE = {roe}")
    print(f"ROA = {roa}")
    print(f"L/A = {la}")
    print()
    print()


def update_company(cur, conn):
    result = choose_company(cur)
    if result is None:
        return
    ticker, _ = result

    ebitda = clean(input("Enter ebitda (in the format '987654321'):\n"))
    sales = clean(input("Enter sales (in the format '987654321'):\n"))
    net_profit = clean(input("Enter net profit (in the format '987654321'):\n"))
    market_price = clean(input("Enter market price (in the format '987654321'):\n"))
    net_debt = clean(input("Enter net debt (in the format '987654321'):\n"))
    assets = clean(input("Enter assets (in the format '987654321'):\n"))
    equity = clean(input("Enter equity (in the format '987654321'):\n"))
    cash_equivalents = clean(input("Enter cash equivalents (in the format '987654321'):\n"))
    liabilities = clean(input("Enter liabilities (in the format '987654321'):\n"))

    cur.execute("""
        UPDATE financial
        SET ebitda = ?, sales = ?, net_profit = ?, market_price = ?, net_debt = ?,
            assets = ?, equity = ?, cash_equivalents = ?, liabilities = ?
        WHERE ticker = ?
    """, (ebitda, sales, net_profit, market_price, net_debt,
          assets, equity, cash_equivalents, liabilities, ticker))

    conn.commit()
    print("Company updated successfully!")
    print()


def delete_company(cur, conn):
    result = choose_company(cur)
    if result is None:
        return
    ticker, _ = result

    cur.execute("DELETE FROM financial WHERE ticker = ?", (ticker,))
    cur.execute("DELETE FROM companies WHERE ticker = ?", (ticker,))
    conn.commit()
    print("Company deleted successfully!")
    print()


def list_companies(cur):
    print("COMPANY LIST")
    cur.execute("SELECT ticker, name, sector FROM companies ORDER BY ticker")
    for ticker, name, sector in cur.fetchall():
        print(f"{ticker} {name} {sector}")
    print()
    print()


# -----------------------------
#       TOP TEN FUNCTIONS
# -----------------------------
def compute_metric(row, metric):
    ebitda, sales, net_profit, market_price, net_debt, assets, equity, cash_eq, liabilities = row

    if metric == "ND/EBITDA":
        if net_debt is not None and ebitda not in (None, 0):
            return net_debt / ebitda

    elif metric == "ROE":
        if net_profit is not None and equity not in (None, 0):
            return net_profit / equity

    elif metric == "ROA":
        if net_profit is not None and assets not in (None, 0):
            return net_profit / assets

    return None


def top_ten(cur, metric):
    cur.execute("""
        SELECT ticker, ebitda, sales, net_profit, market_price, net_debt,
               assets, equity, cash_equivalents, liabilities
        FROM financial
    """)

    rows = cur.fetchall()
    results = []

    for row in rows:
        ticker = row[0]
        metric_value = compute_metric(row[1:], metric)
        if metric_value is not None:
            results.append((ticker, metric_value))

    if metric == "ND/EBITDA":
        results.sort(key=lambda x: x[1], reverse=True)
    else:
        results.sort(key=lambda x: x[1], reverse=True)

    results = results[:10]

    print(f"TICKER {metric}")
    for ticker, value in results:
        print(f"{ticker} {float(f'{value:.2f}')}")
    print()


def top_ten_menu(cur):
    print_top_ten_menu()
    option = input()

    if option == "0":
        return
    elif option == "1":
        top_ten(cur, "ND/EBITDA")
    elif option == "2":
        top_ten(cur, "ROE")
    elif option == "3":
        top_ten(cur, "ROA")
    else:
        print("Invalid option!")
        print()


def crud_menu(cur, conn):
    print_crud_menu()
    option = input()

    if option == "0":
        return
    elif option == "1":
        create_company(cur, conn)
        return
    elif option == "2":
        read_company(cur)
        return
    elif option == "3":
        update_company(cur, conn)
        return
    elif option == "4":
        delete_company(cur, conn)
        return
    elif option == "5":
        list_companies(cur)
        return
    else:
        print("Invalid option!")


def main():
    print("Welcome to the Investor Program!")
    print()

    conn, cur = init_db()

    while True:
        print_main_menu()
        option = input()

        if option == "0":
            print("Have a nice day!")
            break
        elif option == "1":
            crud_menu(cur, conn)
        elif option == "2":
            top_ten_menu(cur)
        else:
            print("Invalid option!")

    conn.close()


if __name__ == "__main__":
    main()