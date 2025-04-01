from database.db import EcomDB
from playwright.sync_api import sync_playwright
import time

def scrape_flipkart(url):
    with sync_playwright() as p:
        # Configure browser to look more human-like
        browser = p.chromium.launch(
            headless=False,  # Set to True after testing
            slow_mo=200,    # Simulate human speed
            channel="chrome"
        )
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1366, "height": 768}
        )
        page = context.new_page()
        
        try:
            # Navigate with extended timeout
            page.goto(url, timeout=90000, wait_until="domcontentloaded")
            time.sleep(3)  # Additional delay
            
            # Handle login popup if it appears
            try:
                page.click("text=✕", timeout=3000)  # Close login popup
                time.sleep(1)
            except:
                pass
            
            # Wait for product name with multiple fallbacks
            try:
                product_name = page.locator("span.B_NuCI").first.inner_text(timeout=15000)
            except:
                product_name = page.locator("h1 span").first.inner_text()
            
            # Price with fallback
            try:
                price = page.locator("div._30jeq3._16Jk6d").first.inner_text(timeout=10000)
            except:
                price = page.locator("div._16Jk6d").first.inner_text()
            
            # Image with fallback
            try:
                image_url = page.locator("img._396cs4._2amPTt").first.get_attribute("src", timeout=5000)
            except:
                image_url = page.locator("img._396cs4").first.get_attribute("src")
            
            # Store in database
            db = EcomDB()
            db.insert_product(
                site="flipkart",
                product_name=product_name.strip(),
                price=price.strip(),
                image_url=image_url,
                product_url=url
            )
            
            return {
                "status": True,
                "data": {
                    "product": product_name.strip(),
                    "price": price.strip(),
                    "image_url": image_url
                }
            }
            
        except Exception as e:
            return {
                "status": False,
                "error": str(e),
                "url": url
            }
        finally:
            browser.close()