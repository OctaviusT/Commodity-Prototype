import sqlite3
from tabulate import tabulate  # pip install tabulate for nice tables

# Connect to the database
conn = sqlite3.connect("finance_prototype.db")
cur = conn.cursor()

# Test: list tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cur.fetchall()
print("Tables in database:")
print(tabulate(tables, headers=["Table Name"], tablefmt="pretty"))

# Test: preview companies
cur.execute("SELECT ticker, name, sector, industry FROM companies LIMIT 5;")
companies = cur.fetchall()
print("\nCompanies sample:")
print(tabulate(companies, headers=["Ticker", "Name", "Sector", "Industry"], tablefmt="pretty"))

# Test: preview financials
cur.execute("SELECT ticker, last_price, pe_ratio, snapshot_time FROM financials ORDER BY snapshot_time DESC LIMIT 5;")
financials = cur.fetchall()
print("\nFinancials sample:")
print(tabulate(financials, headers=["Ticker", "Last Price", "PE Ratio", "Snapshot Time"], tablefmt="pretty"))

conn.close()
