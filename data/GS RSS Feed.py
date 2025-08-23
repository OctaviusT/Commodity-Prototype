import feedparser
import yfinance as yf

# ===============================
# CONFIGURATION
# ===============================
RSS_URL = "https://goldsilver.com/industry-news/feed/"
# Keywords to track for Global South strategy
KEYWORDS = ["gold", "oil", "cobalt", "lithium", "nickel",
            "Africa", "Latin America", "shipping", "freight"]

# Default ticker (easy to swap out)
DEFAULT_TICKER = "GORO"  # Gold Resource Corporation


# ===============================
# FUNCTIONS
# ===============================

def fetch_rss_headlines(rss_url, keywords, top_n=5):
    """Fetch RSS feed and filter for keywords."""
    feed = feedparser.parse(rss_url)
    if not feed.entries:
        return ["⚠️ No RSS entries found. Feed may be down or malformed."]

    filtered = []
    for entry in feed.entries:
        title = entry.get("title", "")
        link = entry.get("link", "")
        if any(word.lower() in title.lower() for word in keywords):
            filtered.append(f"{title} ({link})")

    # Return only the top N
    return filtered[:top_n] if filtered else ["No matching headlines."]


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
        "calls": calls.head(5).to_string(index=False),
        "puts": puts.head(5).to_string(index=False)
    }


# ===============================
# MAIN EXECUTION
# ===============================
if __name__ == "__main__":
    print("=== Filtered Commodity Headlines ===")
    headlines = fetch_rss_headlines(RSS_URL, KEYWORDS)
    for hl in headlines:
        print("•", hl)

    print("\n=== Options Chain Data ===")
    options_data = fetch_options_chain(DEFAULT_TICKER)
    if isinstance(options_data, dict):
        print(f"(Expiry: {options_data['expiry']})")
        print("\n-- Calls --")
        print(options_data["calls"])
        print("\n-- Puts --")
        print(options_data["puts"])
    else:
        print(options_data)
