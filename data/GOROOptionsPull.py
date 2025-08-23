import yfinance as yf
import pandas as pd
from datetime import datetime

# Default ticker (easy to swap out)
DEFAULT_TICKER = "GORO"  # Gold Resource Corporation

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
        "puts": puts    # Include all puts data
    }

# ===============================
# MAIN EXECUTION
# ===============================
options_data = fetch_options_chain(DEFAULT_TICKER)

if isinstance(options_data, dict):
    # Create an Excel writer object
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"options_chain_{DEFAULT_TICKER}_{timestamp}.xlsx"
    
    try:
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            # Write calls data to a sheet
            options_data['calls'].to_excel(writer, sheet_name='Calls', index=False)
            # Write puts data to a separate sheet
            options_data['puts'].to_excel(writer, sheet_name='Puts', index=False)
            # Add a sheet with metadata
            pd.DataFrame({
                'Ticker': [DEFAULT_TICKER],
                'Expiry': [options_data['expiry']],
                'Generated': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            }).to_excel(writer, sheet_name='Metadata', index=False)
        print(f"✅ Excel file '{filename}' saved successfully.")
    except Exception as e:
        print(f"❌ Error saving Excel file: {str(e)}")
else:
    print(options_data)