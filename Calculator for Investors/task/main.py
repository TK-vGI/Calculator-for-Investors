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
    # Load companies.csv (comma-separated)
    if os.path.exists("companies.csv"):
        with open("companies.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = [(r["ticker"], r["name"], r["sector"])
                    for r in reader]
            cur.executemany("INSERT INTO companies (ticker, name, sector) VALUES (?, ?, ?)", rows)


    # Load financial.csv (tab-separated)
    if os.path.exists("financial.csv"):
        with open("financial.csv", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = [
                (r["ticker"], clean(r["ebitda"]), clean(r["sales"]), clean(r["net_profit"]), clean(r["market_price"]),
                 clean(r["net_debt"]), clean(r["assets"]), clean(r["equity"]), clean(r["cash_equivalents"]),
                 clean(r["liabilities"])) for r in reader]
            cur.executemany(
                """ INSERT INTO financial (ticker, ebitda, sales, net_profit, market_price, net_debt, assets, equity,
                                           cash_equivalents, liabilities)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """, rows)


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Create tables if missing
    cur.execute("""
                CREATE TABLE IF NOT EXISTS companies
                (
                    "ticker" TEXT PRIMARY KEY,
                    "name"   TEXT,
                    "sector" TEXT
                )
                """)

    cur.execute("""
                CREATE TABLE IF NOT EXISTS financial
                (
                    "ticker"           TEXT PRIMARY KEY,
                    "ebitda"           REAL,
                    "sales"            REAL,
                    "net_profit"       REAL,
                    "market_price"     REAL,
                    "net_debt"         REAL,
                    "assets"           REAL,
                    "equity"           REAL,
                    "cash_equivalents" REAL,
                    "liabilities"      REAL
                )
                """)

    # Check if DB is empty
    cur.execute("SELECT COUNT(*) FROM companies")
    count = cur.fetchone()[0]
    if count == 0:
        load_csv_data(cur)
        conn.commit()

    return conn, cur


def print_main_menu():
    print(MAIN_MENU)
    print()
    print("Enter an option:")


def print_crud_menu():
    print()
    print(CRUD_MENU)
    print()
    print("Enter an option:")


def print_top_ten_menu():
    print()
    print(TOP_TEN_MENU)
    print()
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
                INSERT INTO financial (ticker, ebitda, sales, net_profit, market_price, net_debt,
                                       assets, equity, cash_equivalents, liabilities)
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
        return "None"
    return f"{value:.2f}"


def read_company(cur):
    result = choose_company(cur)
    if result is None:
        return
    ticker, name = result

    cur.execute("""
                SELECT ebitda,
                       sales,
                       net_profit,
                       market_price,
                       net_debt,
                       assets,
                       equity,
                       cash_equivalents,
                       liabilities
                FROM financial
                WHERE ticker = ?
                """, (ticker,))
    row = cur.fetchone()
    if row is None:
        print("Company not found!")
        print()
        return

    ebitda, sales, net_profit, market_price, net_debt, assets, equity, cash_eq, liabilities = row

    pe = market_price / net_profit if net_profit not in (None, 0) else None
    ps = market_price / sales if sales not in (None, 0) else None
    pb = market_price / assets if assets not in (None, 0) else None
    nd_ebitda = net_debt / ebitda if ebitda not in (None, 0) else None
    roe = net_profit / equity if equity not in (None, 0) else None
    roa = net_profit / assets if assets not in (None, 0) else None
    la = liabilities / assets if assets not in (None, 0) else None

    print(f"{ticker} {name}")
    print(f"P/E = {format_ratio(pe)}")
    print(f"P/S = {format_ratio(ps)}")
    print(f"P/B = {format_ratio(pb)}")
    print(f"ND/EBITDA = {format_ratio(nd_ebitda)}")
    print(f"ROE = {format_ratio(roe)}")
    print(f"ROA = {format_ratio(roa)}")
    print(f"L/A = {format_ratio(la)}")
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
                SET ebitda           = ?,
                    sales            = ?,
                    net_profit       = ?,
                    market_price     = ?,
                    net_debt         = ?,
                    assets           = ?,
                    equity           = ?,
                    cash_equivalents = ?,
                    liabilities      = ?
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


def crud_menu(cur, conn):
    while True:
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


def top_ten_menu():
    while True:
        print_top_ten_menu()
        option = input()
        if option == "0":
            return
        elif option in ("1", "2", "3"):
            print("Not implemented!")
            print()
            return
        else:
            print("Invalid option!")


def main():
    print("Welcome to the Investor Program!")

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
            top_ten_menu()
        else:
            print("Invalid option!")

    conn.close()


if __name__ == "__main__":
    main()
