# src/core/fetcher.py
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError, Error as PlaywrightError

def fetch_html_content(url: str) -> str | None:
    """Fetches HTML content from a given URL using Playwright.

    Args:
        url: The URL to fetch content from.

    Returns:
        The HTML content as a string, or None if fetching fails.
    """
    html_content = None
    try:
        with sync_playwright() as p:
            # Launch a browser (chromium is usually a good default)
            # You might need to run 'playwright install' in your terminal first
            browser = p.chromium.launch()
            page = browser.new_page()
            
            print(f"Navigating to {url} using Playwright...")
            # Navigate to the URL with a reasonable timeout
            page.goto(url, timeout=60000) # 60 seconds timeout
            
            # Wait for the page to be reasonably loaded (optional, might need adjustment)
            # page.wait_for_load_state("networkidle", timeout=30000)
            
            # Get the full HTML content
            html_content = page.content()
            print("Content fetched successfully using Playwright.")
            
            browser.close()
            
        return html_content
        
    except (PlaywrightTimeoutError, PlaywrightError) as e:
        print(f"Error fetching URL {url} with Playwright: {e}")
        if "browser has been closed" not in str(e).lower(): # Avoid printing error if browser closed normally
             if browser: # Ensure browser exists before trying to close
                 try:
                     browser.close()
                 except Exception as close_err:
                     print(f"Error closing browser after fetch error: {close_err}")
        return None
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred during Playwright fetch: {e}")
        # Ensure browser is closed if it exists and wasn't closed
        if browser: 
            try:
                browser.close()
            except Exception as close_err:
                print(f"Error closing browser after unexpected error: {close_err}")
        return None

