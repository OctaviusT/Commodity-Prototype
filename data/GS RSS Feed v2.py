import feedparser
import yfinance as yf
import requests
import pandas as pd
from datetime import datetime

# ===============================
# CONFIGURATION
# ===============================
RSS_URLS = [
    "https://www.mining.com/feed/",
    "https://www.reuters.com/arc/outboundfeeds/news-rss/commodities/?outputType=xml",
    "https://www.spglobal.com/marketintelligence/en/news-insights/rss"
]
KEYWORDS = [
    "gold price", "silver price", "bitcoin mining", "gold exports", "silver exports",
    "Mexico mining", "Brazil mining", "South Africa mining", "Paraguay energy",
    "commodity exports", "mining policy", "trade restrictions", "port logistics",
    "Endeavour Silver", "Bitfarms", "Equinox Gold", "Gold Resource Corp"
]
TICKERS = ["EXK", "BITF", "EQX"]  # Low-priced, liquid for Tier 1 CSPs
UN_COMTRADE_URL = "https://comtrade.un.org/api/get?max=500&type=C&freq=A&px=HS&ps={}&r={}&p=ALL&rg=2&cc={}"

# ===============================
# FUNCTIONS
# ===============================
def fetch_rss_headlines(rss_urls, keywords, top_n=5):
    """Fetch and score RSS headlines based on keyword matches."""
    headlines = []
    for url in rss_urls:
        feed = feedparser.parse(url)
        if not feed.entries:
            print(f"⚠️ No entries from {url}")
            continue
        for entry in feed.entries:
            title = entry.get("title", "").lower()
            link = entry.get("link", "")
            # Score by keyword matches
            score = sum(1 for kw in keywords if kw.lower() in title)
            if score > 0:
                headlines.append({"title": title, "link": link, "score": score})
    
    # Sort by score, limit to top_n
    headlines = sorted(headlines, key=lambda x: x["score"], reverse=True)[:top_n]
    return [f"{h['title']} ({h['link']}) [Score: {h['score']}]" for h in headlines] or ["No matching headlines."]

def fetch_comtrade_data(country_code, hs_code, year=datetime.now().year):
    """Fetch trade data from UN Comtrade for signal validation."""
    url = UN_COMTRADE_URL.format(year, country_code, hs_code)
    try:
        response = requests.get(url, timeout=5)
        data = response.json().get('dataset', [])
        if data:
            df = pd.DataFrame(data)
            return df['tradeValue'].sum()
        return 0
    except Exception as e:
        print(f"⚠️ Comtrade error: {e}")
        return 0

def fetch_options_chain(ticker_symbol):
    """Fetch options chain for nearest expiry."""
    ticker = yf.Ticker(ticker_symbol)
    try:
        expiry = ticker.options[0]
        options = ticker.option_chain(expiry)
        calls = options.calls[["strike", "lastPrice", "bid", "ask", "volume", "openInterest", "impliedVolatility"]]
        puts = options.puts[["strike", "lastPrice", "bid", "ask", "volume", "openInterest", "impliedVolatility"]]
        return {
            "expiry": expiry,
            "calls": calls.head(5).to_string(index=False),
            "puts": puts.head(5).to_string(index=False)
        }
    except IndexError:
        return f"⚠️ No options data for {ticker_symbol}"

def generate_trade_signal(ticker, headlines, country_code, hs_code):
    """Generate trade signal based on headlines and trade data."""
    export_value = fetch_comtrade_data(country_code, hs_code)
    prior_value = fetch_comtrade_data(country_code, hs_code, datetime.now().year - 1)
    has_relevant_news = any(ticker.lower() in hl.lower() or "export" in hl.lower() for hl in headlines)
    
    if export_value > 1.1 * prior_value and has_relevant_news:
        return f"Strong bullish signal for {ticker} – consider selling cash-secured put."
    elif has_relevant_news:
        return f"Moderate signal for {ticker} – review news for put sale."
    return f"No clear signal for {ticker}."

# ===============================
# MAIN EXECUTION
# ===============================
if __name__ == "__main__":
    print("=== Filtered Commodity Headlines ===")
    headlines = fetch_rss_headlines(RSS_URLS, KEYWORDS)
    for hl in headlines:
        print("•", hl)

    print("\n=== Trade Signals and Options Data ===")
    ticker_configs = [
        ("EXK", "484", "7106"),  # Mexico, silver
        ("BITF", "600", "2716"),  # Paraguay, energy
        ("EQX", "76", "7108")     # Brazil, gold
    ]
    for ticker, country_code, hs_code in ticker_configs:
        print(f"\n--- {ticker} ---")
        signal = generate_trade_signal(ticker, headlines, country_code, hs_code)
        print(signal)
        options_data = fetch_options_chain(ticker)
        if isinstance(options_data, dict):
            print(f"(Expiry: {options_data['expiry']})")
            print("-- Calls --")
            print(options_data["calls"])
            print("\n-- Puts --")
            print(options_data["puts"])
        else:
            print(options_data)