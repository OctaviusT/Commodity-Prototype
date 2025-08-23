import sqlite3
import yfinance as yf
from datetime import datetime

# --- Database Setup ---
conn = sqlite3.connect("finance_prototype.db")
cursor = conn.cursor()

# Create companies table (basic metadata)
cursor.execute("""
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT UNIQUE,
    name TEXT,
    sector TEXT,
    industry TEXT
)
""")

# Create financials snapshot table
cursor.execute("""
CREATE TABLE IF NOT EXISTS financials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    last_price REAL,
    volume INTEGER,
    market_cap REAL,
    pe_ratio REAL,
    pb_ratio REAL,
    eps REAL,
    roe REAL,
    profit_margin REAL,
    dividend_yield REAL,
    beta REAL,
    debt_to_equity REAL,
    current_ratio REAL,
    free_cash_flow REAL,
    earnings_date TEXT,
    snapshot_time TEXT NOT NULL,
    FOREIGN KEY (ticker) REFERENCES companies(ticker)
)
""")

conn.commit()

# --- Helper Functions ---
def insert_company_metadata(ticker_obj, ticker_symbol):
    """Insert company metadata into companies table if not exists"""
    info = ticker_obj.info
    cursor.execute("""
    INSERT OR IGNORE INTO companies (ticker, name, sector, industry)
    VALUES (?, ?, ?, ?)
    """, (
        ticker_symbol,
        info.get("longName"),
        info.get("sector"),
        info.get("industry")
    ))
    conn.commit()

def insert_financial_snapshot(ticker_obj, ticker_symbol):
    """Insert financial snapshot into financials table"""
    info = ticker_obj.info
    snapshot_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
    INSERT INTO financials (
        ticker, last_price, volume, market_cap,
        pe_ratio, pb_ratio, eps, roe, profit_margin,
        dividend_yield, beta, debt_to_equity, current_ratio,
        free_cash_flow, earnings_date, snapshot_time
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        ticker_symbol,
        info.get("currentPrice"),
        info.get("volume"),
        info.get("marketCap"),
        info.get("trailingPE"),
        info.get("priceToBook"),
        info.get("trailingEps"),
        info.get("returnOnEquity"),
        info.get("profitMargins"),
        info.get("dividendYield"),
        info.get("beta"),
        info.get("debtToEquity"),
        info.get("currentRatio"),
        info.get("freeCashflow"),
        str(info.get("nextEarningsDate")),  # sometimes None
        snapshot_time
    ))
    conn.commit()

# --- Test Run ---
tickers = ["TSN", "CLF", "DUK"]  # Tyson, Cleveland-Cliffs, Duke Energy
for symbol in tickers:
    t = yf.Ticker(symbol)
    insert_company_metadata(t, symbol)
    insert_financial_snapshot(t, symbol)

conn.close()
