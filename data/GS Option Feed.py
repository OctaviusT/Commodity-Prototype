import yfinance as yf
import pandas as pd
from datetime import datetime

# List of tickers for global south strategy
TICKERS = ["GORO", "LODE", "FSM", "BTG", "TGB"]

def fetch_options_chain(ticker_symbol):
    """Fetch options chain for given ticker (nearest expiry)."""
    ticker = yf.Ticker(ticker_symbol)
    try:
        expiry = ticker.options[0]  # nearest expiry
    except IndexError:
        return "⚠️ No options data available."

    options = ticker.option_chain(expiry)
    calls = options.calls[["strike", "lastPrice", "bid", "ask", "volume", "openInterest", "impliedVolatility"]]
    puts = options.puts[["strike", "lastPrice", "bid", "ask", "volume", "openInterest", "impliedVolatility"]]

    return {
        "expiry": expiry,
        "calls": calls,  # Include all calls data
        "puts": puts     # Include all puts data
    }

# ===============================
# MAIN EXECUTION
# ===============================
data = {}
for ticker in TICKERS:
    options_data = fetch_options_chain(ticker)
    data[ticker] = options_data

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"options_chains_global_south_{timestamp}.xlsx"

try:
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        metadata_list = []
        for ticker, options_data in data.items():
            if isinstance(options_data, dict):
                calls_sheet = f"{ticker}_Calls"
                options_data['calls'].to_excel(writer, sheet_name=calls_sheet, index=False)
                
                puts_sheet = f"{ticker}_Puts"
                options_data['puts'].to_excel(writer, sheet_name=puts_sheet, index=False)
                
                metadata_list.append({
                    'Ticker': ticker,
                    'Expiry': options_data['expiry'],
                    'Status': 'Success',
                    'Generated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
            else:
                metadata_list.append({
                    'Ticker': ticker,
                    'Expiry': None,
                    'Status': options_data,
                    'Generated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })
        
        if metadata_list:
            metadata_df = pd.DataFrame(metadata_list)
            metadata_df.to_excel(writer, sheet_name='Metadata', index=False)
    
    print(f"✅ Excel file '{filename}' saved successfully.")
except Exception as e:
    print(f"❌ Error saving Excel file: {str(e)}")