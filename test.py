# playwright_scroll_scrape.py
from playwright.sync_api import sync_playwright
import time
import csv

def scroll_to_bottom(page, pause=1.0, max_scrolls=100):
    """Scrolls page to bottom repeatedly until no more height increases or max_scrolls reached."""
    previous_height = page.evaluate("() => document.body.scrollHeight")
    for i in range(max_scrolls):
        page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(pause)
        new_height = page.evaluate("() => document.body.scrollHeight")
        if new_height == previous_height:
            # maybe a bit more wait in case content loads slowly
            time.sleep(pause * 2)
            new_height = page.evaluate("() => document.body.scrollHeight")
            if new_height == previous_height:
                break
        previous_height = new_height

def extract_items(page):
    """
    Example extractor that finds list items with a CSS selector and returns text.
    Change selector to match the site you target.
    """
    elements = page.query_selector_all("div.item")  # <- change to site-specific selector
    results = []
    for el in elements:
        title = el.query_selector("h2")  # example
        summary = el.query_selector("p.summary")
        results.append({
            "title": title.inner_text().strip() if title else "",
            "summary": summary.inner_text().strip() if summary else ""
        })
    return results

def main(url, headless=True):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(user_agent="Mozilla/5.0 (compatible; MyScraper/1.0)")
        page = context.new_page()
        page.set_default_navigation_timeout(60_000)  # 60s
        page.goto(url)

        # Optional: wait for a container or spinner to appear/disappear
        # page.wait_for_selector("div.content", timeout=15_000)

        scroll_to_bottom(page, pause=1.0, max_scrolls=200)

        # Now extract data
        items = extract_items(page)

        # Save to CSV
        with open("results_playwright.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["title", "summary"])
            writer.writeheader()
            writer.writerows(items)

        print(f"Extracted {len(items)} items. Saved to results_playwright.csv")

        browser.close()

if __name__ == "__main__":
    # Replace this with the page you want to scrape
    target_url = "https://www.dailydoseofds.com/a-crash-course-on-building-rag-systems-part-1-with-implementations/"
    main(target_url, headless=True)
