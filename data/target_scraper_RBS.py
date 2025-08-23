# requirements.txt
# playwright==1.43.0
# (after install: run `playwright install`)

from playwright.sync_api import sync_playwright # type: ignore
import time
import random
import json


# ---------- Utility Functions ----------
def random_user_agent():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/114.0.0.0 Safari/537.36"
    ]
    return random.choice(agents)

def human_delay(min_sec=1, max_sec=3):
    time.sleep(random.uniform(min_sec, max_sec))


# ---------- Scraper Core ----------
def scrape_target():
    scraped_data = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set to True for automation
        context = browser.new_context(user_agent=random_user_agent())
        page = context.new_page()

        print("Opening Target meat/seafood category...")
        page.goto("https://www.target.com/c/meat-seafood-grocery/-/N-5xsyh", timeout=60000)
        human_delay()

        # Wait for products to load
        page.wait_for_selector('[data-test="product-card"]', timeout=15000)
        items = page.query_selector_all('[data-test="product-card"]')

        print(f"Found {len(items)} products")
        for item in items[:10]:  # Limit for now to 10 items for testing
            try:
                title = item.query_selector("h3").inner_text()
                price = item.query_selector('[data-test="product-price"]').inner_text()
                scraped_data.append({"name": title, "price": price})
            except Exception as e:
                print(f"Error parsing item: {e}")

        # Save data
        with open("data/raw_output.json", "w", encoding="utf-8") as f:
            json.dump(scraped_data, f, indent=2)

        print("Scraping complete. Data saved to data/raw_output.json")
        browser.close()


if __name__ == "__main__":
    scrape_target()
