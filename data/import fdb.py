import sqlite3

conn = sqlite3.connect("finance_prototype.db")
cursor = conn.cursor()

# Example: read from companies
cursor.execute("SELECT * FROM companies LIMIT 10;")
print("Companies:", cursor.fetchall())

# Example: read from financials
cursor.execute("SELECT * FROM financials LIMIT 10;")
print("Financials:", cursor.fetchall())

conn.close()
